import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime

mongo_client = MongoClient("mongodb://localhost:27017/")

def on_connect(client, userdata, flags, rc):
    print("Conectado com código " + str(rc))
    client.subscribe("/sensor-iot-unisinos-send")
    print("Conexão realizada com sucesso!")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

    payload = json.loads(msg.payload.decode("utf-8"))

    temperature = payload["temperature"]
    umidity = payload["humidity"]
    brightness = payload["brightness"]

    send_information_to_sensor(temperature, umidity, brightness)
    
    handle_temperature(temperature)
    handle_umidity(umidity)
    handle_brightness(brightness)

def send_information_to_sensor(temperature, umidity, brightness):
    message_to_send = { "tempIsOutRange": is_temperature_out_range(temperature),
                        "umiIsOutRange": is_umidity_out_range(umidity),
                        "brigIsOutRange": is_temperature_out_range(brightness)}
    
    print(f"\nMensagem enviada: {message_to_send}")
    client.publish("/sensor-iot-unisinos-receive", json.dumps(message_to_send), qos=2)

def handle_temperature(temperature):
    db = mongo_client["iot_farm"]
    collection = db["temperature"]
    collection.insert_one({"temperature": temperature, "created": datetime.now()})

def handle_umidity(umidity):
    db = mongo_client["iot_farm"]
    collection = db["humidity"]
    collection.insert_one({"humidity": umidity, "created": datetime.now()})

def handle_brightness(brightness):
    db = mongo_client["iot_farm"]
    collection = db["brightness"]
    collection.insert_one({"brightness": brightness, "created": datetime.now()})
    
def is_temperature_out_range(temperature):
    return (temperature < 10 or temperature > 25)

def is_umidity_out_range(umidity):
    return (umidity < 70 or umidity > 80)

def is_brightness_out_range(brightness):
    return (brightness < 10)

if __name__ == "__main__":
    client = mqtt.Client(client_id="PythonClient-iot-unisinos-1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("iot-broker", "iot-broker")
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_forever()
