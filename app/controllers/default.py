from app import app
from flask import jsonify, request, render_template
from app.account import Account
import requests
from app.models.lamportclock import Vector_Clock
import socket
import json

banks = {
    1: {
        'name': 'Banco Santander',
        'host': '127.0.0.1',
        'port': 5001
    },
    2: {
        'name': 'Nubank',
        'host': '127.0.0.1',
        'port': 5002
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
    return "HELLO " + str(user)


@app.route("/login", methods=['POST'])
def login():
    my_clock.event()
    data = request.get_json()

    """id = data["id"]
    account_number = data["account_number"]
    balance = data["balance"]
    name = data["name"]
    password = data["password"]
    cpf = data["cpf"]

    aux_acc = Account(id, account_number, balance, name, password, cpf)"""

    # return render_template('login.html')


@app.route("/lastEvent", methods=['GET'])
def get_clock():
    return jsonify(my_clock.clock)

# Consultar todas as contas


@app.route('/accounts/', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def obtein_accounts():
    return jsonify(accounts)


# Consultar uma conta dado um id
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id):
    return account_by_id(id)


def account_by_id(id):
    return jsonify(accounts[id])


# Atualizar os dados de uma conta dado um id
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


# Excluir uma conta
@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    for index, account in enumerate(accounts):
        if account.get('id') == id:
            del accounts[index]

    return jsonify(accounts)


@app.route("/accounts/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    to_account = int(data["account_id"])

    account_exists_here = to_account in accounts
    if account_exists_here:
        account = accounts[to_account]
        account["balance"] += float(data["value"])  # Tá sa
        return jsonify(account)

    return jsonify({"error": "Account doesnt exist in this bank!"})


@app.route("/accounts/credit", methods=["POST"])
def credit():
    data = request.get_json()
    account = int(data["account_id"])
    value = data["value"]

    account_exists_here = account in accounts
    if account_exists_here:
        account = accounts[account]
        account["balance"] -= float(value)

        requests.post(f"{request.remote_addr}", json=account)

        return jsonify({account})

    return jsonify({"error": True})


@app.route("/accounts/transactions", methods=["POST"])
def transactions():
    data = request.get_json()
    # Já dá pra incorporar aqui a delegação.

    from_account = int(data["from_account_id"])
    to_account = int(data["to_account_id"])
    value = float(data["value"])

    # Se a conta pra fazer a retirada pertencer a este banco:
    if from_account in accounts:
        account_a = accounts[from_account]
        # Se a conta pra fazer o deposito também pertencer a este banco:
        if to_account in accounts:

            account_b = accounts[to_account]

            account_a["balance"] -= data["value"]
            account_b["balance"] += data["value"]

            return jsonify(account_a, account_b)
        else:
            # Se não, tem que procurar
            message = {
                "account_id": to_account,
                "value": value
            }

            # for bank in banks:
            # f'http://{banks[bank]["host"]}:{banks[bank]["port"]}/credit'

            headers = {'Content-Type': 'application/json'}
            url = 'http://127.0.0.1:5001/credit'

            res = requests.post(url, json=message, headers=headers)
            data = res.json()

            if not data["error"]:
                account_a["balance"] -= data["value"]
                return jsonify(account_a, data)

            # Não encontrou em nenhum outro banco
            return jsonify({"error": True})
    # Se não, ocorre uma delegação
    else:
        pass


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

    response = requests.post(url, data=payload, headers=headers)

    return response.json()
