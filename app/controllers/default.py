from app import app
from flask import jsonify, request, render_template
from app.account import Account


# Casos na comunicação entre bancos:
# - Conta no Banco A manda pix para conta no Banco B
# Todos os nós tem uma signature (key) para verificar se a chave é uma chave pix válida

# É importante colocar também o banco?
# Quando uso chaves invés de colchetes da esse erro: <TypeError: unhashable type: 'dict'>
accounts = [
    {
        'id': 1,
        'name': 'Roberto Firmino da Silva Siqueira',
        'account_number': '140110-5',
        'account_type': 'particular',
        'balance': 122.45,
        'cpf': '836.715.920-11',
        'password': '1234'
    },

    {
        'id': 2,
        'name': 'Gundogan Pereira dos Santos',
        'account_number': '136114-0',
        'account_type': 'particular',
        'balance': 0.0,
        'cpf': '498.623.780-85',
        'password': '1234'
    },
    {
        'id': 3,
        'name': 'Pep Guardiola Neto',
        'account_number': '771324-12',
        'account_type': 'particular',
        'balance': '4527.12',
        'cpf': '128.960.537-42',
        'password': '1234'
    }
]


@app.route('/index/<user>', methods=['GET'])
@app.route('/<user>', methods=['GET'])
@app.route('/index', methods=['GET'], defaults={'user': None})
@app.route('/', methods=['GET'], defaults={'user': None})
def index(user):
    return render_template('base.html',
                           user=user)


@app.route("/signup", methods=['POST'])
def login():

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

    return render_template('index.html')

# Consultar todas as contas


@app.route('/accounts/', methods=['GET'])
@app.route('/accounts', methods=['GET'])
def obtein_accounts():
    return jsonify(accounts)

# Consultar uma conta dado um id


@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id):
    for account in accounts:
        if account.get('id') == id:
            return jsonify(account)


# Atualizar os dados de uma conta dado um id

''


@app.route('/accounts/<int:id>', methods=['PUT'])
def edit_account_by_id(id):
    changed_account = request.get_json()
    for index, account in enumerate(accounts):
        if account.get('id') == id:
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

# função Valida a chave


def validate_key(key):
    # Preciso da signature aqui
    pass


@app.route('/accounts/<int:id>/newkey')
def generate_random_pix_key(id):

    data = request.get_json()
    id = data["id"]

    # se existir uma conta com esse id
    if id:
        return make_pix_key(data["cpf"])


def make_pix_key(cpf):
    # Bcrypt aqui?
    pass


# Ciclo de uma transação de envio:
# - Cliente logado solicita enviar pix
# - Checar saldo
# - Se sa

# @app.route('/accounts/<int: id>/value')
def send_pix():
    pass
