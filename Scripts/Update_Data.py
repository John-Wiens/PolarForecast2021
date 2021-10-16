
import re
import numpy as np
import math

from Types.Match import build_match
from Types.Team import build_team
from Types.Ranking import Rank, Rankings

import TBA
import DB_Access as db
from Process_Data import build_score_matrix, solve_matrix, get_climb_results, get_prob
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
            
            if event['event_code'] == 'catt':
            #if today >= start and today <= end or force_update:# or event['event_code'] == 'cacg'  #isjo
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

    db_teams = sorted(db_teams, key=lambda k: float(k['key']))

    event = db.find_one('events',event_code)
    event['teams'] = teams
    db.update_one('events', event)

    return db_teams


def update_calculations(event_code, matches, teams, force_update = False):
    rankings, is_updated = TBA.get("/event/"+event_code+"/rankings")
    team_list = [float(team['key']) for team in teams]
    team_array, score_array = build_score_matrix(event_code, team_list, matches)
    endgame_array = get_climb_results(team_list, matches)
    if np.count_nonzero(score_array)==0:
        db.log_msg(f"Data Array is Empty for {event_code}. Exiting")
        return
    
    #team_powers = IRLS(score_array, team_array,1)
    team_powers = solve_matrix(team_array,score_array)
    
    estimator_scores = team_array @ team_powers
    estimator_error = np.square(score_array - estimator_scores) # Compute Squared Errors
    team_variances = solve_matrix(team_array, estimator_error) # Compute Each Teams contribution to squared error
    
    

    #team_powers = np.matmul(np.linalg.pinv(team_array),score_array)
    team_powers[np.isnan(team_powers)] = 0
    team_powers = np.around(team_powers,decimals = 2)

    team_variances[np.isnan(team_variances)] = 0
    #team_variances = np.around(team_variances,decimals = 2)
    index = 0
    opr_matrix = team_powers[:,0] + team_powers[:,1] + endgame_array[:,0] + team_powers[:,3]
    variance_matrix = team_variances[:,0] + team_variances[:,1] + endgame_array[:,3] + team_variances[:,3]
    cell_variance = team_variances[:,4] + team_variances[:,5] + team_variances[:,6]
    max_opr = np.max(opr_matrix)
    for team in teams:
        opr = opr_matrix[index]
        pr = 100 * (opr/max_opr)
        bpm = team_powers[index][4] + team_powers[index][5] + team_powers[index][6]

        try:
            team['power']= pr
            team['opr']= opr
            team['climb_percent'] = endgame_array[index][2]
            team['score_variance'] = variance_matrix[index]
            team['climb_variance'] = endgame_array[index][3]
            team['cell_variance'] = cell_variance[index]
            team['auto_pr']= team_powers[index][0]
            team['control_pr']= team_powers[index][1]
            team['endgame_pr']= endgame_array[index][0]
            team['cell_pr']= team_powers[index][3]
            team['cell_count']= bpm
            team['extra_rp']= team_powers[index][8]
            team['fouls'] = team_powers[index][7]
            index +=1
            db.update_one('teams', team)
            
        except Exception as e:
            db.log_msg("Issue Updating Team Power Rankings"+ team+ str(e))
        
    
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

def clean_num(num):
    if num is None:
        return 0
    else:
        return num

def get_climb_probs(probs):
    single_climb_prob = min(sum(probs),1)
    double_climb_prob = max(probs[1] * probs[2], max(probs[0] * probs[1], probs[0]*probs[2]))
    tripple_climb_prob = probs[0] * probs[1] * probs[2]
    return single_climb_prob, double_climb_prob, tripple_climb_prob


def update_match_predictions(event, matches, teams):
    for match in matches:
        if match['results'] == 'Predicted':

            predicted_blue_cells = 0
            predicted_red_cells = 0
            
            predicted_blue_endgame = 0
            predicted_red_endgame = 0

            blue_variance = 0
            red_variance = 0

            blue_climb_probs = []
            red_climb_probs = []

            blue_cell_variance = 0
            red_cell_variance = 0
            
            match["blue_extra_rp"] = 0
            match["red_extra_rp"] = 0
            for i in range(0,3):
                try:
                    blue_team = db.find_one('teams', match['blue'+str(i)])
                    red_team = db.find_one('teams', match['red'+str(i)])

                    match["blue_score"] += clean_num(blue_team["opr"])
                    match["blue_auto_score"] += clean_num(blue_team["auto_pr"])
                    match["blue_control_score"] += clean_num(blue_team["control_pr"])
                    match["blue_endgame_score"] += clean_num(blue_team["endgame_pr"])
                    match["blue_cell_score"] += clean_num(blue_team["cell_pr"])
                    match["blue_auto_score"] += clean_num(blue_team["auto_pr"])
                    blue_variance += blue_team["score_variance"]
                    blue_climb_probs.append(blue_team["climb_percent"])
                    blue_cell_variance += blue_team["cell_variance"]

                    match["red_score"] += clean_num(red_team["opr"])
                    match["red_auto_score"] += clean_num(red_team["auto_pr"])
                    match["red_control_score"] += clean_num(red_team["control_pr"])
                    match["red_endgame_score"] += clean_num(red_team["endgame_pr"])
                    match["red_cell_score"] += clean_num(red_team["cell_pr"])
                    match["red_auto_score"] += clean_num(red_team["auto_pr"])
                    red_variance += red_team["score_variance"]
                    red_climb_probs.append(red_team["climb_percent"])
                    red_cell_variance += red_team["cell_variance"]


                    predicted_blue_cells += clean_num(blue_team["cell_count"])
                    predicted_blue_endgame += clean_num(blue_team["endgame_pr"])

                    predicted_red_cells += clean_num(red_team["cell_count"])
                    predicted_red_endgame += clean_num(red_team["endgame_pr"])
                except:
                    blue_climb_probs.append(0)
                    red_climb_probs.append(0)
            
            match['blue_cell_rp_prob'] = get_prob( match["blue_cell_score"]- 50, blue_cell_variance)
            match['red_cell_rp_prob'] = get_prob(match["red_cell_score"] - 50, red_cell_variance)

            blue_single, blue_double, blue_tripple = get_climb_probs(blue_climb_probs)
            red_single, red_double, red_tripple = get_climb_probs(red_climb_probs)

            if blue_single > 0.75 or blue_double > 0.5 or blue_tripple > 0.5:
                match["blue_score"] +=15
            if red_single > 0.75 or red_double > 0.5 or red_tripple > 0.5:
                match["red_score"] +=15

            match['blue_climb_rp_prob'] = min(blue_double + blue_tripple, 1)
            match['red_cell_rp_prob'] = min(red_double + red_tripple, 1)



            if blue_double >= 0.5 or blue_tripple > 0.5:
                match["blue_rp"] +=1

            if red_double >= 0.5 or red_tripple > 0.5:
                match["red_rp"] +=1

            if predicted_blue_cells >= 50:
                match["blue_rp"] +=1

            if predicted_red_cells >= 50:
                match["red_rp"] +=1

            win_margin = match["blue_score"] - match["red_score"]
            win_variance = blue_variance + red_variance

            #win_prob = 0.5 * math.erfc(-win_margin/math.sqrt(2*win_variance))
            win_prob = get_prob(win_margin, win_variance)

            if match["blue_score"] > match["red_score"]:
                match["blue_rp"] +=2
                match["win_prob"] = win_prob
            elif match["red_score"] > match["blue_score"]:
                match["red_rp"] +=1
                match["win_prob"] = 1 - win_prob
            else:
                match["blue_rp"] +=1
                match["red_rp"] +=1
                match["win_prob"] = 0
            

            match["predicted_blue_score"] = clean_num(match["blue_score"])
            match["predicted_red_score"] = clean_num(match["red_score"])
             
            match['results'] = match['win_prob']
            #print(match['key'], match['blue_score'], match['red_score'], match['win_prob'])
            db.update_one('matches', match)

def update_rank_predictions(matches, teams):
    rps = {}
    if len(matches) !=0:
        for match in matches:
            if match['results'] == 'Actual':
                for i in range(0,3):
                    blue_team = match['blue'+str(i)]
                    if blue_team in rps:
                        rps[blue_team] += 0
                    else:
                        rps[blue_team] = 0

            else:
                pass
    else:
        pass


def update_data():
    if(TBA.check_connection()):
        events = update_events(force_update = False)
        for event in events:
            matches = update_matches(event)
            teams = update_teams(event)
            update_calculations(event, matches, teams)
            update_match_predictions(event, matches, teams)
            #update_rank_predictions(matches, teams)
            print(matches)

if __name__ == '__main__':
    update_data()

        
