from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Selecionar a base de dados
db = client["iot_farm"]

# Criar as coleções
db.create_collection("temperature")
db.create_collection("humidity")
db.create_collection("brightness")

print("Coleções criadas com sucesso!")