# Primeiro-Dashboard-Streamlit
import streamlit as st
import pandas as pd
import numpy as np

# Título do Dashboard
st.title('Meu Primeiro Dashboard em Streamlit')

# Nome da coluna de data/hora
DATE_COLUMN = 'date/time'
# URL do conjunto de dados da Uber
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Função para carregar os dados com cache, evitando recarregamento desnecessário
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)  # Lê as primeiras 'nrows' linhas do CSV
    lowercase = lambda x: str(x).lower()       # Converte nomes das colunas para minúsculas
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])  # Converte a coluna de data/hora para datetime
    return data

# Exibe mensagem de carregamento dos dados
data_load_state = st.text('Carregando os dados...')
data = load_data(10000)  # Carrega 10.000 linhas do dataset
data_load_state.text('Carregando os dados... pronto!')

# Exibe os dados brutos
st.subheader('Dados brutos')
st.write(data)

# Exibe gráfico com o número de corridas por hora
st.subheader('Número de corridas por hora')

# Cria um histograma com base na hora das corridas
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Exibe o mapa com todas as corridas
st.subheader('Mapa de todas as corridas')
st.map(data)

# Controle deslizante para escolher a hora
hour_to_filter = st.slider('Escolha a hora para filtrar corridas', 0, 23, 17)  # min: 0h, max: 23h, padrão: 17h

# Filtra os dados de acordo com a hora selecionada
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Exibe o mapa das corridas filtradas pela hora
st.subheader(f'Mapa das corridas às {hour_to_filter}:00')
st.map(filtered_data)