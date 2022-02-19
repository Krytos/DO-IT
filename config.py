import os
from pymongo import MongoClient


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    client = MongoClient(os.environ.get("MONGODB_URI"))
    MONGODB_SETTINGS = {
        'db': 'alex',
        'host': os.environ.get("MONGODB_URI")
    }