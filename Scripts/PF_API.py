from typing import Optional
from fastapi import FastAPI
import pymongo
from datetime import datetime
import DB_Access as db
from fastapi.middleware.cors import CORSMiddleware

uri = "mongodb://root:example@0.0.0.0:27017/"
client = pymongo.MongoClient(uri)


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/events/{event_key}/matches")
def read_item(event_key: str, comp_level: str = None):
    filters = {'event_key':event_key}
    if comp_level:
        filters['comp_level'] = comp_level
    response = db.find('matches', filters)
    if response is not None:
        data = []
        for entry in response:
            del entry['_id']
            data.append(entry)
        return {'data': data}
    else:
        return 404



