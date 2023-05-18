from flask import Flask, jsonify, request

app = Flask(__name__)

accounts = [
    {
        'id': 1,
        'name': 'Roberto Firmino da Silva Siqueira',
        'bank': 'Banco do Brasil',
        'agency': '0041-8',
        'account': '140110-5',
        'initial_balance': '122.45',
        'cpf': '836.715.920-11'
    },
    {
        'id': 2,
        'name': 'Gundogan Pereira dos Santos',
        'bank': 'Banco do Brasil',
        'agency': '0041-8',
        'account': '136114-0',
        'initial_balance': '0.0',
        'cpf': '498.623.780-85'
    },
    {
        'id': 3,
        'name': 'Pep Guardiola Neto',
        'bank': 'Santander',
        'agency': '9941-2',
        'account': '771324-12',
        'initial_balance': '4527.12',
        'cpf': '128.960.537-42'
    }
]

# Rota inicial


@app.route('/', methods=['GET'])
def home():
    return jsonify('Welcome to the app!')

# Consultar(todas)


@app.route('/accounts', methods=['GET'])
def obtein_accounts():
    return jsonify(accounts)

# Consultar(id)


@app.route('/accounts/<int:id>', methods=['GET'])
def get_account_by_id(id):
    for account in accounts:
        if account.get('id') == id:
            return jsonify(account)

# Editar


@app.route('/accounts/<int:id>', methods=['PUT'])
def edit_account_by_id(id):
    changed_account = request.get_json()
    for index, account in enumerate(accounts):
        if account.get('id') == id:
            accounts[index].update(changed_account)
            return jsonify(accounts[index])

# Criar


@app.route('/accounts', methods=['POST'])
def add_new_account():
    new_account = request.get_json()
    accounts.append(new_account)

    return jsonify(accounts)

# Excluir


@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    for index, account in enumerate(accounts):
        if account.get('id') == id:
            del accounts[index]

    return jsonify(accounts)


app.run(port=5000, host='localhost', debug=True)