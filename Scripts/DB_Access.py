import pymongo
import config
from datetime import datetime

client = pymongo.MongoClient(config.DB_URI)


def log_msg(msg, type = 'INFO',):
    event = {
        'DateTime' : datetime.now(),
        'Message': msg,
        'Type': type
    }
    print("DBLog", event)
    insert_one('Log', event)
    

def insert_one(col, item):
    db = client['pf-database']
    col = db[col]
    return col.insert_one(item)


def update_one(col, item):
    db = client['pf-database']
    col = db[col]
    return col.replace_one({'key': item['key']}, item, upsert=True)

def find_one(col, filter):
    db = client['pf-database']
    col = db[col]
    return col.find_one({'key':str(filter)})

def find(col, filter):
    db = client['pf-database']
    col = db[col]
    return col.find(filter)