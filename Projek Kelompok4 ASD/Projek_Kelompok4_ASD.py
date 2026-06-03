import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.json")

print("Database:", DATABASE)
print("Lokasi program:", os.getcwd())
print("File ditemukan?", os.path.exists(DATABASE))