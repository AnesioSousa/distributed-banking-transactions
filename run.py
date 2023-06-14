from app import app
import requests
import time


def handle_menu():
    PORT = 5001
    connections = [f'http://127.0.0.1:5001',
                   f'http://127.0.0.1:5002', f'http://127.0.0.1:5003']

    opc = None
    while opc != "6":
        time.sleep(2)
        print("######################################")
        print("# 1 - Gerar node ID ")
        print("# 2 - Iniciar rede P2P (no inicial)")
        print("# 3 - Entrar em uma rede P2P ")
        print("# 4 - Sair da rede P2P")
        print("# 5 - Mostrar informacoes do No")
        print("# 7 - Send message")
        print("# 6 - Sair da aplicacao")
        print("#####################################")
        opc = input('digite sua opc:')

        if int(opc) == 7:
            for url in connections:
                try:
                    response = requests.get(url)
                    if response.ok:
                        dictt = response.json()
                        print(dictt)
                        print()
                        print()
                        print()
                except requests.exceptions.ConnectionError:
                    print(f'Falha ao conectar em:{url}')


if __name__ == "__main__":
    # handle_menu()
    app.run(port=5001, host='127.0.0.1')
