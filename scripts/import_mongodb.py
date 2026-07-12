from bson import json_util
from pymongo import MongoClient
from pathlib import Path

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "streaming"

LISTENS_PATH = "data/processed/listens.json"
USERS_PATH = "data/processed/users.json"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

documents = json_util.loads(Path(LISTENS_PATH).read_text(encoding="utf-8"))
users = json_util.loads(Path(USERS_PATH).read_text(encoding="utf-8"))

db['ecoutes'].drop()
db['utilisateurs'].drop()

db['ecoutes'].insert_many(documents)
db['utilisateurs'].insert_many(users)

print(f"ecoutes: {db['ecoutes'].count_documents({})}")
print(f"utilisateurs: {db['utilisateurs'].count_documents({})}")
print(db['ecoutes'].find_one())