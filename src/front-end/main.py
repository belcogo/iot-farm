import streamlit as st
from pymongo import MongoClient
import pandas as pd
import time

# Conexão com o MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_farm"]

# Função para buscar dados do MongoDB
def fetch_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclui o campo _id
    data_frame = pd.DataFrame(data)
    data_frame = data_frame.sort_values("created", ascending=False)
    return data_frame

# Configuração do título do app
st.title("IoT Farm Dashboard")

# Exibir dados de temperatura
st.header("Temperatura")
temperature_data = fetch_data("temperature")
temperature_data["created"] = pd.to_datetime(temperature_data["created"])
temperature_data["created_formatted"] = temperature_data["created"].dt.strftime("%H:%M:%S")
st.dataframe(temperature_data)

# Exibir dados de umidade
st.header("Umidade")
humidity = fetch_data("humidity")
humidity["created"] = pd.to_datetime(humidity["created"])
humidity["created_formatted"] = humidity["created"].dt.strftime("%H:%M:%S")
st.dataframe(humidity)

# Exibir dados de luminosidade
st.header("Luminosidade")
brightness_data = fetch_data("brightness")
brightness_data["created"] = pd.to_datetime(brightness_data["created"])
brightness_data["created_formatted"] = brightness_data["created"].dt.strftime("%H:%M:%S")
st.dataframe(brightness_data)

# Gráficos
st.subheader("Gráficos")
if not temperature_data.empty:
    st.line_chart(temperature_data.set_index("created_formatted")["temperature"], use_container_width=True)
if not humidity.empty:
    st.line_chart(humidity.set_index("created_formatted")["humidity"], use_container_width=True)
if not brightness_data.empty:
    st.line_chart(brightness_data.set_index("created_formatted")["brightness"], use_container_width=True)

time.sleep(5)
st.rerun()