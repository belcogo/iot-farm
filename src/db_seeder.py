from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Selecionar a base de dados
db = client["iot_farm"]

# Deletar todos os dados das coleções
db["temperature"].delete_many({})
db["humidity"].delete_many({})
db["brightness"].delete_many({})

# Adicionar dados a coleção temperature
temperature = db["temperature"]
temperature.insert_one({"temperature": 20, "created": "2025-03-26 14:30:45.123456"})
temperature.insert_one({"temperature": 21, "created": "2025-03-26 14:30:46.123456"})
temperature.insert_one({"temperature": 22, "created": "2025-03-26 14:30:47.123456"})
temperature.insert_one({"temperature": 23, "created": "2025-03-26 14:30:48.123456"})


# Adicionar dados a coleção humidity
humidity = db["humidity"]
humidity.insert_one({"humidity": 75, "created": "2025-03-26 14:30:45.123456"})
humidity.insert_one({"humidity": 76, "created": "2025-03-26 14:30:46.123456"})
humidity.insert_one({"humidity": 76, "created": "2025-03-26 14:30:47.123456"})
humidity.insert_one({"humidity": 77, "created": "2025-03-26 14:30:48.123456"})

# Adicionar dados a coleção brightness
brightness = db["brightness"]
brightness.insert_one({"brightness": 15, "created": "2025-03-26 14:30:45.123456"})
brightness.insert_one({"brightness": 15, "created": "2025-03-26 14:30:46.123456"})
brightness.insert_one({"brightness": 15, "created": "2025-03-26 14:30:47.123456"})
brightness.insert_one({"brightness": 15, "created": "2025-03-26 14:30:48.123456"})

print("Dados inseridos com sucesso!")

# Mostrar os últimos dados inseridos em temperature
print("Últimos dados inseridos em temperature:")
for t in temperature.find().sort("created", -1).limit(2):
    print(t)