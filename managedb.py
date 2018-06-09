from pymongo import MongoClient
import config

def get_db():
    dbname = config.DATABASE_CONFIG['dbname']
    mongo_url = config.DATABASE_CONFIG['mongo_url']
    client = MongoClient(mongo_url)
    db = client[dbname]
    return db