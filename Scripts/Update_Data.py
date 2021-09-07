
import re
import numpy as np
import azure.functions as func
from Types.Match import build_match
from Types.Team import build_team
from Types.Ranking import Rank, Rankings
import TBA
import DB_Access as db
from Process_Data import build_score_matrix, solve_matrix
from datetime import datetime




def get_as_date(date)   :
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
            
            db.update_one('events', event)

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
    team_list = [float(team['key']) for team in teams]
    team_array, score_array, endgame_array = build_score_matrix(event_code, team_list, matches)
    if np.count_nonzero(score_array)==0:
        db.log_msg(f"Data Array is Empty for {event_code}. Exiting")
        return
    
    #team_powers = IRLS(score_array, team_array,1)
    team_powers = solve_matrix(team_array,score_array)
    #team_powers = np.matmul(np.linalg.pinv(team_array),score_array)
    team_powers[np.isnan(team_powers)] = 0
    team_powers = np.around(team_powers,decimals = 2)

    index = 0
    opr_matrix = team_powers[:,0] + team_powers[:,1] + endgame_array[:,0] + team_powers[:,3]
    max_opr = np.max(opr_matrix)
    team_list = []
    for team in teams:
        opr = opr_matrix[index]
        pr = 100 * (opr/max_opr)
        bpm = team_powers[index][4] + team_powers[index][5] + team_powers[index][6]
        try:
            team['power']= pr
            team['opr']= opr
            team['auto_pr']= team_powers[index][0]
            team['control_pr']= team_powers[index][1]
            team['endgame_pr']= endgame_array[index][0]
            team['cell_pr']= team_powers[index][3]
            team['cell_count']= bpm
            team['extra_rp']= team_powers[index][8]
            team['fouls'] = team_powers[index][7]
            
            updated_team = db.update_one('teams', team)
            index +=1
        except Exception as e:
            db.log_msg("Issue Updating Team Power Rankings"+ team+ str(e))
        
        event = db.find_one('events',event_code)
        event['teams'] = teams
        db.update_one('events', event)
    
    # Update Rankings Table
    try:
        table = []
        teams = np.array(team_list)
        
        for ranking in rankings["rankings"]:

            team = float((ranking["team_key"])[3:])
            index = np.searchsorted(teams, team)
            opr = opr_matrix[index]
            
            pr = 100 * (opr/max_opr)
            bpm = team_powers[index][4] + team_powers[index][5] + team_powers[index][6]
            rank = float(ranking["rank"])
            row = {"team": team, "rank": rank, "opr": opr, "auto":team_powers[index][0], "control":team_powers[index][1], "endgame":endgame_array[index][0], "cells": team_powers[index][3], "bpm":bpm, "fouls":team_powers[index][8], "power":pr}
            table.append(Rank(**row))
        rankings = Rankings(**{'key': event_code, 'rankings':table})
        db.update_one('rankings', rankings.dict())                          
            
    except Exception as e:
        db.log_msg("Issue Updating Event Update Time", event_code, str(e))
        raise

    

def update_match_predictions(event, matches, teams):
    for match in matches:
        if match['results'] == 'Predicted':

            predicted_blue_cells = 0
            predicted_red_cells = 0
            
            predicted_blue_endgame = 0
            predicted_red_endgame = 0
            
            match["blue_extra_rp"] = 0
            match["red_extra_rp"] = 0
            for i in range(0,3):
                
                blue_team = db.find_one('teams', match['blue'+str(i)])
                red_team = db.find_one('teams', match['red'+str(i)])

                match["blue_score"] += blue_team["opr"]
                match["blue_auto_score"] += blue_team["auto_pr"]
                match["blue_control_score"] += blue_team["control_pr"]
                match["blue_endgame_score"] += blue_team["endgame_pr"]
                match["blue_cell_score"] += blue_team["cell_pr"]
                match["blue_auto_score"] += blue_team["auto_pr"]

                match["red_score"] += red_team["opr"]
                match["red_auto_score"] += red_team["auto_pr"]
                match["red_control_score"] += red_team["control_pr"]
                match["red_endgame_score"] += red_team["endgame_pr"]
                match["red_cell_score"] += red_team["cell_pr"]
                match["red_auto_score"] += red_team["auto_pr"]



                predicted_blue_cells += blue_team["cell_count"]
                predicted_blue_endgame += blue_team["endgame_pr"]

                predicted_red_cells += red_team["cell_count"]
                predicted_red_endgame += red_team["endgame_pr"]
                
            if predicted_blue_endgame >= 50:
                match["blue_rp"] +=1
            if predicted_red_endgame >= 50:
                match["red_rp"] +=1
            if predicted_blue_cells >= 49:
                match["blue_rp"] +=1
            if predicted_red_cells > 49:
                match["red_rp"] +=1
            if match["blue_score"] > match["red_score"]:
                match["blue_rp"] +=2
            elif match["red_score"] > match["blue_score"]:
                match["red_rp"] +=1
            else:
                match["blue_rp"] +=1
                match["red_rp"] +=1
            
            match["predicted_blue_score"] =  match["blue_score"]
            match["predicted_red_score"] =  match["red_score"]
            db.update_one('matches', match)


def update_data():
    if(TBA.check_connection()):
        events = update_events(force_update = False)
        for event in events:
            matches = update_matches(event)
            teams = update_teams(event)
            update_calculations(event, matches, teams)
            update_match_predictions(event, matches, teams)

def main(mytimer: func.TimerRequest) -> None:
    update_data()


if __name__ == '__main__':
    update_data()

        
