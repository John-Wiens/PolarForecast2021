from typing import Optional
from fastapi import FastAPI
import pymongo
from datetime import datetime
import DB_Access as db


uri = "mongodb://root:example@0.0.0.0:27017/"
client = pymongo.MongoClient(uri)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/teams/{team}")
def read_item(team: str):
    response = db.find_one('teams', team)
    if response is not None:
        del response['_id']
        return response
    else:
        return 404

@app.get("/events/{event_key}/rankings")
def read_item(event_key: str):
    response = db.find_one('rankings', event_key)
    if response is not None:
        del response['_id']
        return response
    else:
        return 404

@app.get("/events/{event_key}/matches/{match_key}")
def read_item(event_key: str, match_key: str):
    response = db.find_one('matches', match_key)
    if response is not None:
        del response['_id']
        return response
    else:
        return 404


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