import streamlit as st
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar conexão com o banco de dados PostgreSQL
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

try:
    conn = psycopg2.connect(host=db_host, user=db_user, password=db_password, dbname=db_name)
    cursor = conn.cursor()
except Exception as e:
    st.error("Erro ao conectar ao banco de dados PostgreSQL. Verifique suas credenciais.")
    st.stop()

# Função para exibir vendas por CNPJ
def display_sales_by_cnpj(cnpj):
    cursor.execute(f"SELECT * FROM dados_api WHERE cnpj = '{cnpj}'")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['amount', 'category_id', 'cnpj', 'sale_id', 'sale_date', 'value'])
        st.write(f"Vendas para o CNPJ: {cnpj}")
        st.dataframe(df)
    else:
        st.warning("Nenhuma venda encontrada para o CNPJ selecionado.")

# Função para exibir gráfico de série temporal
def display_time_series_plot(cnpj):
    cursor.execute(f"SELECT sale_date, value FROM dados_api WHERE cnpj = '{cnpj}'")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['sale_date', 'value'])
        df['sale_date'] = pd.to_datetime(df['sale_date'])

        plt.figure(figsize=(10, 6))
        plt.plot(df['sale_date'], df['value'])
        plt.xlabel('Data da Venda')
        plt.ylabel('Valor')
        plt.title(f"Série Temporal de Vendas para o CNPJ: {cnpj}")
        st.pyplot(plt)
    else:
        st.warning("Nenhuma venda encontrada para o CNPJ selecionado.")

# Aplicativo Streamlit
st.title("Visualização de Vendas por CNPJ")

# Exibir vendas por CNPJ
selected_cnpj = st.text_input("Digite o CNPJ desejado:")
if st.button("Exibir Vendas"):
    display_sales_by_cnpj(selected_cnpj)

# Exibir gráfico de série temporal
selected_cnpj_time_series = st.text_input("Digite o CNPJ para o gráfico de série temporal:")
if st.button("Exibir Gráfico de Série Temporal"):
    display_time_series_plot(selected_cnpj_time_series)
