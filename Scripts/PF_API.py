
import DB_Access as db
import azure.functions as func
from typing import Optional
from fastapi import FastAPI
from http_asgi import AsgiMiddleware
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:4200",
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
            filters['comp_level'] = { '$not': 'qm' }
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

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
