import TBA
import DB_Access as db


import re

from Types.Match import build_match
from Types.Team import build_team
from Process_Data import build_score_matrix, solve_matrix
from datetime import datetime



def get_as_date(date):
    return datetime.strptime(date, '%Y-%m-%d')


def update_events(force_update = False):
    today = datetime.now()
    raw_events, is_updated = TBA.get('/events/2021')
    event_list = []
    for event in raw_events:
        try:
            start = get_as_date(event['start_date'])
            end = get_as_date(event['end_date'])
            
            if today >= start and today <= end or event['event_code'] == 'isjo' or force_update:
                event_list.append(event['key'])
                #db.insert_one(event)

        except Exception as e:
            message = f"Error in Query_TBA.py. Unable to Query {event['event_code']}"
            db.log_msg(message)

    return event_list

            
    
def update_matches(event_code, force_update = False):
    matches, is_updated = TBA.get('/event/'+event_code+'/matches')
    max_match_num = 0
    match_num_regex = re.compile("m[0-9]+")
    db_matches = []
    for match in matches:
        db_match = build_match(match)
        span = match_num_regex.search(match["key"]).span()
        match_num = float(match["key"][span[0]+1:span[1]])
        if match_num > max_match_num:
            max_match_num = match_num
        if db_match is not None:
            as_dict = db_match.dict() # Force the pydantic type for type checking
            db.update_one('matches', as_dict)
            db_matches.append(as_dict)
    return db_matches


def update_teams(event_code, force_update = False):
    teams, is_updated = TBA.get("/event/"+event_code+"/teams")
    db_teams = []
    for team in teams:
        db_team = build_team(team) # Force the pydantic type for type checking
        if db_team is not None:
            as_dict = db_team.dict()
            db.update_one('teams', as_dict)
            db_teams.append(as_dict)
    return db_teams


def update_calculations(event_code, matches, teams, force_update = False):
    rankings, is_updated = TBA.get("/event/"+event_code+"/rankings")
    team_array, score_array, endgame_array = build_score_matrix(event_code, teams, matches)
    pass



if __name__ == '__main__':
    if(TBA.check_connection()):
        events = update_events()
        for event in events:
            matches = update_matches(event)
            teams = update_teams(event)
            update_calculations(event, matches, teams)

        
