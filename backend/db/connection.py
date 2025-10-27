from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Lee la URI de conexión desde el archivo .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "jwt_analysis"

# Crear conexión con MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_collection():
    """
    Retorna la colección donde se guardarán los resultados.
    """
    return db["tests"]
