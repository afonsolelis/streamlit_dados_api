# Use uma imagem base do Python
FROM python:3.11

# Configurar variáveis de ambiente
ENV DEBIAN_FRONTEND=noninteractive

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requisitos do aplicativo e instalá-los
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do aplicativo para o container
COPY . .

# Instalar o Streamlit (caso não esteja nos requisitos)
RUN pip install streamlit

# Expor a porta que o Streamlit irá ouvir (padrão é 8501)
EXPOSE 8501

# Comando para iniciar o aplicativo Streamlit
CMD ["streamlit", "run", "app.py"]
