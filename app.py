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

# Função para exibir vendas por CNPJ e data
def display_sales_by_cnpj_and_date(cnpj, start_date, end_date):
    cursor.execute(f"SELECT * FROM dados_api WHERE cnpj = '{cnpj}' AND sale_date BETWEEN '{start_date}' AND '{end_date}'")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['amount', 'category_id', 'cnpj', 'sale_id', 'sale_date', 'value'])
        st.write(f"Vendas para o CNPJ: {cnpj} no período de {start_date} a {end_date}")
        st.dataframe(df)
    else:
        st.warning("Nenhuma venda encontrada para o CNPJ e datas selecionados.")

# Função para exibir gráfico de série temporal
def display_time_series_plot(cnpj, start_date, end_date):
    cursor.execute(f"SELECT sale_date, value FROM dados_api WHERE cnpj = '{cnpj}' AND sale_date BETWEEN '{start_date}' AND '{end_date}'")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['sale_date', 'value'])
        df['sale_date'] = pd.to_datetime(df['sale_date'])

        plt.figure(figsize=(10, 6))
        plt.plot(df['sale_date'], df['value'])
        plt.xlabel('Data da Venda')
        plt.ylabel('Valor')
        plt.title(f"Série Temporal de Vendas para o CNPJ: {cnpj} no período de {start_date} a {end_date}")
        st.pyplot(plt)
    else:
        st.warning("Nenhuma venda encontrada para o CNPJ e datas selecionados.")

# Função para exibir os 10 CNPJs que mais vendem em um gráfico de barra horizontal
def display_top_10_selling_cnpjs():
    cursor.execute("SELECT cnpj, SUM(value) AS total_sales FROM dados_api GROUP BY cnpj ORDER BY total_sales DESC LIMIT 10")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['cnpj', 'total_sales'])
        plt.figure(figsize=(10, 6))
        plt.barh(df['cnpj'], df['total_sales'])
        plt.xlabel('Total de Vendas')
        plt.ylabel('CNPJ')
        plt.title('Top 10 CNPJs que Mais Vendem')
        st.pyplot(plt)
    else:
        st.warning("Nenhum dado encontrado para exibir o gráfico.")

# Aplicativo Streamlit
st.title("Visualização de Vendas por CNPJ e Data")

# Seleção de CNPJ
selected_cnpj = st.text_input("Digite o CNPJ desejado:")

# Seleção de datas
start_date = st.date_input("Selecione a data de início:")
end_date = st.date_input("Selecione a data de término:")

if st.button("Exibir Vendas"):
    display_sales_by_cnpj_and_date(selected_cnpj, start_date, end_date)

if st.button("Exibir Gráfico de Série Temporal"):
    display_time_series_plot(selected_cnpj, start_date, end_date)

# Exibir gráfico dos 10 CNPJs que mais vendem
if st.button("Exibir Top 10 CNPJs que Mais Vendem"):
    display_top_10_selling_cnpjs()
