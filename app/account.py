

class Account:
    bank = 'Banco Central do Brasil'
    all = []

    class Pix_key:
        def __init__(self, cpf, key):
            self.cpf = cpf
            self.key = key

    # FATO: Há contas particulares e contas conjuntas

    def __init__(self, id, account_number, balance, name, password, cpf):
        self.__id = id
        self.__number = account_number
        self.__balance = float(balance)
        self.__password = password
        self.__cpf = cpf
        self.__pix_keys = []

        Account.all.append(self)

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value > 3000:  # and self.account_type == 'Corrente':
            raise Exception(
                "The inserted value exceeds the maximum value permited by this type of account!")
        else:
            self.__balance = value

    @classmethod
    def create_pix_key(self):
        return "chave gerada aqui"

    def __repr__(self):
        return f"Account('{self.__bank}', '{self.__agency}', '{self.__number}', '{self.__balance}')"
