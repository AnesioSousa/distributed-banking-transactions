import asyncio
from app import app
from flask import jsonify, request, render_template
from app.account import Account
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from app.models.lamportclock import Vector_Clock
import socket
import json

# Casos na comunicação entre bancos:
# - Conta no Banco A manda pix para conta no Banco B
# Todos os nós tem uma signature (key) para verificar se a chave é uma chave pix válida

# É importante colocar também o banco?
# Quando uso chaves invés de colchetes da esse erro: <TypeError: unhashable type: 'dict'>

banks = {
    1: {
        'name': 'Banco Santander',
        'host': 'localhost',
        'port': 5002
    },
    2: {
        'name': 'Nubank',
        'host': 'localhost',
        'port': 5003
    }
}


accounts = {
    0: {
        'name': 'Roberto Firmino da Silva Siqueira',
        'account_number': '140110-5',
        'account_type': 'particular',
        'balance': 122.45,
        'cpf': '836.715.920-11',
        'password': '1234'
    },
    1: {
        'name': 'Gundogan Pereira dos Santos',
        'account_number': '136114-0',
        'account_type': 'particular',
        'balance': 0.0,
        'cpf': '498.623.780-85',
        'password': '1234'
    },
    2: {
        'name': 'Pep Guardiola Neto',
        'account_number': '771324-12',
        'account_type': 'particular',
        'balance': 4527.12,
        'cpf': '128.960.537-42',
        'password': '1234'
    }
}

my_clock = Vector_Clock(0, 3)


@app.route('/index/<user>', methods=['GET'])
@app.route('/<user>', methods=['GET'])
@app.route('/index', methods=['GET'], defaults={'user': None})
@app.route('/', methods=['GET'], defaults={'user': None})
def index(user):
    my_clock.event()
    return "HELLO"


@app.route("/login", methods=['POST', 'GET'])
def login():
    my_clock.event()
    data = request.get_json()

    id = data["id"]
    account_number = data["account_number"]
    balance = data["balance"]
    name = data["name"]
    password = data["password"]
    cpf = data["cpf"]

    aux_acc = Account(id, account_number, balance, name, password, cpf)

    if id == 3:
        return "Peguei você!"

    return render_template('login.html')

# Consultar todas as contas


@app.route('/accounts/', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def obtein_accounts():
    my_clock.event()
    return jsonify(accounts)


@app.route("/lastEvent", methods=['GET'])
def get_clock():
    return jsonify({"event": my_clock.clock})

# Consultar uma conta dado um id


@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id):
    return account_by_id(id)


def account_by_id(id):
    return jsonify(accounts[id])


# Atualizar os dados de uma conta dado um id
''


@app.route('/accounts/<int:id>', methods=['PUT'])
def edit_account_by_id(id):
    changed_account = request.get_json()
    for index, account in enumerate(accounts):
        if account_by_id(id) == id:
            accounts[index].update(changed_account)
            return jsonify(accounts[index])

# Criar uma conta


@app.route('/accounts', methods=['POST'])
def add_new_account():
    new_account = request.get_json()
    accounts.append(new_account)

    return jsonify(accounts)


def get_bank_by_user_id():
    pass


@app.route("/accounts/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    to_account = int(data["account_id"])
    value = float(data["value"])

    account_exists_here = to_account in accounts
    if account_exists_here:
        account = accounts[to_account]
        account["balance"] += float(data["value"])  # Tá sa
        return jsonify(account)

    return jsonify({"error": "Account doesnt exist in this bank!"})


@app.route("/accounts/transactions", methods=["POST"])
def transactions():
    data = request.get_json()
    # Já dá pra incorporar aqui a delegação.

    from_account = int(data["from_account_id"])
    to_account = int(data["to_account_id"])
    value = float(data["value"])
    # Se a conta é desse banco
    # Se não é, de onde é? Vou precisar saber o banco pra poder conversar com ele

    from_bank = get_bank_by_user_id(from_account)
    to_bank = get_bank_by_user_id(to_account)

    # Tem que separar os casos de chegada de requisição aqui. Tá misturando tudo. Casos:
    #

    if from_bank == 0:  # O próprio
        # if from_account == to_account:
        account_exists_here = to_account in accounts
        if account_exists_here:
            account = accounts[to_account]

            if data["increase"]:  # É de quem está mandando!
                r = requests.post()
                deposit(account, value)
                account["balance"] += float(data["value"])  # Tá sa

            else:
                account["balance"] -= float(data["value"])
            return jsonify(account)  # Já retorna direto o 200?
        else:
            return jsonify({"error": "Account doesnt exist in this bank!"})
            # Depósito
    else:
        # Onde entra o broadcast? (se for preciso usar)
        url = f'http://{banks[from_bank]}:5000/transaction'

        message = {
            "from_account_id": from_account,
            "to_account_id": to_account,
            "value": value
        }

        # Verificar atomicidade
        r = requests.post(url, json=message)

        # if r.ok:

    return jsonify({"error": 'some error occurred'})


# Excluir uma conta
@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    for index, account in enumerate(accounts):
        if account.get('id') == id:
            del accounts[index]

    return jsonify(accounts)


@app.route("/accounts/transaction", methods=['POST'])
def transaction():
    data = request.get_json()

    from_account = int(data["from_account"])
    to_account = int(data["to_account_id"])
    value = float(data["value"])

    url = 'http://127.0.0.1:5001/accounts/increase'

    message = {
        "account": to_account,
        "value": value
    }

    # Tem que continuar tentando. Não pode executar nada além daqui (Atomicidade)
    response = requests.post(url, json=message)
    res_data = response.json()

    if response.ok:
        accounts[from_account]["balance"] -= value

        return jsonify(res_data)

    return jsonify({"error": 'some error occurred'})


# um cliente pode tranferir dinheiro entre contas de bancos diferentes
@app.route('/bank/delegate_transfer', methods=['POST'])
def delegate_transfer():
    my_clock.event()

    data = request.get_json()

    bank_c = request.remote_addr
    bank_c_port = request.environ.get('REMOTE_PORT')

    bank_a = data["sender_bank"]
    bank_a_sender_account = data["sender_account"]
    # IDEIA: Usar chaves pix -> pix_key = data["receiver_pix_key"]
    bank_b_account_id = data["account_id"]
    value = data["value"]

    bank = banks[bank_a]
    print(bank["host"]+':'+str(bank["port"]))
    url = f'http://{bank["host"]}:{bank["port"]}/'

    message = {
        "requester_bank": 0,
        "clock": my_clock.clock,
        "sender_account": bank_a_sender_account,
        "pix_key": bank_b_account_id,
        "value": value
    }

    response = requests.post(url, json=message)

    if response.status_code == 200:
        return
    else:
        pass

    ip = socket.gethostbyname(socket.gethostname())

    data = {
        "host": ip,
    }

    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(data)

    response = requests.post(url_destino, data=payload, headers=headers)

    return r.json()

    # é 404 msm? Acho que tem que ser erro do cliente!

#
