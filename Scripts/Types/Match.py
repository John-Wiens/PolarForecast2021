from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Match(BaseModel):

    key: str
    update_time: float = datetime.utcnow().timestamp()
    results: str

    comp_level: str
    event_key: str
    match_number: int
    set_number: int
    time: int
    blue0: int
    red0: int
    blue1: int
    red1: int
    blue2: int
    red2: int

    blue_score: float
    blue_score: float
    blue_auto_score: float 
    blue_control_score: float 
    blue_endgame_score: float 
    blue_cell_score: float 
    blue_inner_goals: float 
    blue_high_goals: float 
    blue_low_goals: float 
    blue_endgame_robot1: str 
    blue_endgame_robot2: str 
    blue_endgame_robot3: str 
    blue_fouls: float
    blue_rp: float
    blue_extra_rp: float 

    red_score: float
    red_score: float
    red_auto_score: float 
    red_control_score: float 
    red_endgame_score: float 
    red_cell_score: float 
    red_inner_goals: float 
    red_high_goals: float 
    red_low_goals: float 
    red_endgame_robot1: str 
    red_endgame_robot2: str 
    red_endgame_robot3: str 
    red_fouls: float
    red_rp: float
    red_extra_rp: float

def build_match(match):
    for i in range(0,3):
        match["blue" + str(i)] = match["alliances"]["blue"]["team_keys"][i][3:]
        match["red" + str(i)] = match["alliances"]["red"]["team_keys"][i][3:]
        
    if match["score_breakdown"] != "null" and match["score_breakdown"] is not None:  
        match["blue_score"] = match["alliances"]["blue"]["score"]
        match["blue_auto_score"] = match["score_breakdown"]["blue"]["autoPoints"]
        match["blue_control_score"] = match["score_breakdown"]["blue"]["controlPanelPoints"]
        match["blue_endgame_score"] = match["score_breakdown"]["blue"]["endgamePoints"]
        match["blue_cell_score"] = match["score_breakdown"]["blue"]["teleopCellPoints"]
        match["blue_inner_goals"] = match["score_breakdown"]["blue"]["teleopCellsInner"]
        match["blue_high_goals"] = match["score_breakdown"]["blue"]["teleopCellsOuter"]
        match["blue_low_goals"] = match["score_breakdown"]["blue"]["teleopCellsBottom"]
        match["blue_endgame_robot1"] = match["score_breakdown"]["blue"]["endgameRobot1"]
        match["blue_endgame_robot2"] = match["score_breakdown"]["blue"]["endgameRobot2"]
        match["blue_endgame_robot3"] = match["score_breakdown"]["blue"]["endgameRobot3"]
        match["blue_fouls"] = match["score_breakdown"]["red"]["foulPoints"]
        match["blue_rp"] = match["score_breakdown"]["blue"]["rp"]
        match["blue_extra_rp"] = 0
        
        match["red_score"] = match["alliances"]["red"]["score"]
        match["red_auto_score"] = match["score_breakdown"]["red"]["autoPoints"]
        match["red_control_score"] = match["score_breakdown"]["red"]["controlPanelPoints"]
        match["red_endgame_score"] = match["score_breakdown"]["red"]["endgamePoints"]
        match["red_cell_score"] = match["score_breakdown"]["red"]["teleopCellPoints"]
        match["red_inner_goals"] = match["score_breakdown"]["red"]["teleopCellsInner"]
        match["red_high_goals"] = match["score_breakdown"]["red"]["teleopCellsOuter"]
        match["red_low_goals"] = match["score_breakdown"]["red"]["teleopCellsBottom"]
        match["red_endgame_robot1"] = match["score_breakdown"]["red"]["endgameRobot1"]
        match["red_endgame_robot2"] = match["score_breakdown"]["red"]["endgameRobot2"]
        match["red_endgame_robot3"] = match["score_breakdown"]["red"]["endgameRobot3"]
        match["red_fouls"] = match["score_breakdown"]["red"]["foulPoints"]
        match["red_rp"] = match["score_breakdown"]["red"]["rp"]
        match["red_extra_rp"] = 0
        
        match["results"] = "Actual"
        
        # Compute what RP is extra and what RP is comp
        if match["blue_score"] > match["red_score"]:
            match["blue_extra_rp"] = max(match["blue_rp"] - 2,0)
            match["red_extra_rp"] = max(match["blue_rp"],0)
        elif match["red_score"] > match["blue_score"]:
            match["blue_extra_rp"] = max(match["blue_rp"], 0)
            match["red_extra_rp"] = max(match["blue_rp"] - 2, 0)
        else:
            match["blue_extra_rp"] = max(match["blue_rp"] - 1,0)
            match["red_extra_rp"] = max(match["blue_rp"] - 1,0)
    
        
        del match["alliances"]
        del match["videos"]
        del match["score_breakdown"]
        del match["winning_alliance"]

        db_match = Match(**match)
        return db_match
    return None



        