# Usar uma imagem base do Python
FROM python:3.9-slim

# Configurar o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copiar o arquivo de dependências e instalar pacotes
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do serviço
COPY app/ ./app

# Comando para rodar o servidor com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

