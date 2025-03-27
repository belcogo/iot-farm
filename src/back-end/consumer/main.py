import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime

mongo_client = MongoClient("mongodb://localhost:27017/")

def on_connect(client, userdata, flags, rc):
    print("Conectado com código " + str(rc))
    client.subscribe("/sensor-iot-unisinos")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

    payload = json.loads(msg.payload.decode("utf-8"))

    temperature = payload["temperature"]
    umidity = payload["umidity"]
    brightness = payload["brightness"]
    
    handle_temperature(temperature)
    handle_umidity(umidity)
    handle_brightness(brightness)

def handle_temperature(temperature):
    db = mongo_client["iot_farm"]
    collection = db["temperature"]
    collection.insert_one({"temperature": temperature, "created": datetime.now()})

    if temperature < 10 or temperature > 25:
        print("Temperatura fora do intervalo ideal!")
        # Enviar notificação para broker.
    else:
        print("Temperatura dentro do intervalo ideal!")
        # Enviar notificação para broker.

def handle_umidity(umidity):
    db = mongo_client["iot_farm"]
    collection = db["umidity"]
    collection.insert_one({"umidity": umidity, "created": datetime.now()})

    if umidity < 70 or umidity > 80:
        print("Humidade fora do intervalo ideal!")
        # Enviar notificação para broker.
    else:
        print("Humidade dentro do intervalo ideal!")
        # Enviar notificação para broker.

def handle_brightness(brightness):
    db = mongo_client["iot_farm"]
    collection = db["brightness"]
    collection.insert_one({"brightness": brightness, "created": datetime.now()})

    if brightness < 10:
        print("Está denoite!")
        # Enviar notificação para broker.
    else:
        print("Está de dia!")
        # Enviar notificação para broker.

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Conectar no broker MQTT 
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_forever()
