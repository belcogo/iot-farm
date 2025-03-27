import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Conexão com o MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_farm"]

# Função para buscar dados do MongoDB
def fetch_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclui o campo _id
    return pd.DataFrame(data)

# Configuração do título do app
st.title("IoT Farm Dashboard")

# Exibir dados de temperatura
st.header("Temperatura")
temperature_data = fetch_data("temperature")

st.dataframe(temperature_data)

# Exibir dados de umidade
st.header("Umidade")
humidity = fetch_data("humidity")
st.dataframe(humidity)

# Exibir dados de luminosidade
st.header("Luminosidade")
brightness_data = fetch_data("brightness")
st.dataframe(brightness_data)

# Gráficos
st.subheader("Gráficos")
if not temperature_data.empty:
    st.line_chart(temperature_data.set_index("created")["temperature"], use_container_width=True)
if not humidity.empty:
    st.line_chart(humidity.set_index("created")["humidity"], use_container_width=True)
if not brightness_data.empty:
    st.line_chart(brightness_data.set_index("created")["brightness"], use_container_width=True)