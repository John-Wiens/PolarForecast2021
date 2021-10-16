
import DB_Access as db
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi_utils.tasks import repeat_every
from Update_Data import update_data

app = FastAPI()

run_analysis = True

origins = [
    "http://localhost",
    "http://localhost:4200",
    "https://polarforecastfrc.com",
    "*"
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

@app.get("/events")
def read_item():
    filters = {'event_type':99}
    response = db.find('events', filters)
    if response is not None:
        data = []
        for entry in response:
            if 'teams' in entry:
                del entry['teams']
            if '_id' in entry:
                del entry['_id']
            
            data.append(entry)
        return {'data': data}
    else:
        return 404

@app.get("/teams/{team}")
def read_item(team: str):
    response = db.find_one('teams', team)
    if response is not None:
        del response['_id']
        return response
    else:
        return 404

@app.get("/events/{event_key}")
def read_item(event_key: str):
    response = db.find_one('events', event_key)
    if response is not None:
        del response['_id']
        return response
    else:
        return 404

@app.get("/events/{event_key}/rankings")
def read_item(event_key: str):
    response = db.find_one('rankings', event_key)
    print(response)
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
        if comp_level == 'elim':
            filters['comp_level'] = { '$not': {'$eq':'qm'}}
        else:
            filters['comp_level'] = comp_level
    print(filters)
    response = db.find('matches', filters)
    if response is not None:
        data = []
        for entry in response:
            del entry['_id']
            data.append(entry)
        return {'data': data}
    else:
        return 404

@app.on_event("startup")
@repeat_every(seconds=60*10)
def update_database():
    if run_analysis:
        #update_data()
        pass


