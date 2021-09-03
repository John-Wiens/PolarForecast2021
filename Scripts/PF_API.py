from typing import Optional
from fastapi import FastAPI
import pymongo
from datetime import datetime



uri = "mongodb://root:example@0.0.0.0:27017/"
client = pymongo.MongoClient(uri)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/user_location/")
def write_item(longitude: float, latitude: float, user_id:int):
    mydb = client['test-database']
    mycol = mydb['Container1']
    event = {
        'Longitude': longitude,
        'latitude': latitude,
        'DateTime': datetime.utcnow()
    }
    mycol.insert_one(event)
    return 200