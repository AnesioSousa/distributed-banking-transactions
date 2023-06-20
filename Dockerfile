FROM python:3-alpine

# Copia todo o diretório atual para a pasta /cloud dentro do container
COPY . /app

# Esse comando é como o comando 'cd' no terminal
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000/tcp

# Define o comando padrão para executar a aplicação
CMD ["python", "run.py"]