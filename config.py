import os
from pymongo import MongoClient


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Importiert Secret Key aus .env
    client = MongoClient(os.environ.get("MONGODB_URI"))  # Importiert Datenbank URI aus .env
    MONGODB_SETTINGS = {
        'db': 'alex',
        'host': os.environ.get("MONGODB_URI")
    }