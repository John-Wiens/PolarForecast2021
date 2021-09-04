import json
import numpy as np
import decimal
import datetime
import TBA
from scipy.optimize import nnls


# A is the condition Matrix
# y is the output matrix
# p is the order norm to solve with
def IRLS(y, A, p):
    x = np.random.rand(A.shape[1],y.shape[1])
    last_error = float("inf")
    
    iterations = 0
    while iterations < 10:
        e = y - np.matmul(A,  x)
        e_len = e.shape[0]
        w = np.power(e,(p-2)/2);
        W = np.matmul(w,np.linalg.pinv(np.array([sum(w)])))
        W = np.diag(W[:,0])
        
        x_new = np.matmul(np.matmul(np.matmul(np.linalg.pinv(np.matmul(np.matmul(A.T,W),A)),A.T),W),y)
        error = np.linalg.norm(y - np.matmul(A,x_new),p)
        if error < last_error:
            x = x_new
            last_error = error
        else:
            break
        iterations +=1
    return x

def calc_schedule_strengths(event_key, match_data, teams, team_powers, num_matches):
    schedules = np.zeros(len(teams),1)
    teams = np.array(teams)
    for i in range(0, num_matches):
        key_str = event_key+"_qm" + str(i+1)
        match = match_data.get_item(Key={'key': key_str})
        match = match["Item"]
        
        b0 = np.searchsorted(teams, float(match["blue"+str(0)]))
        b1 = np.searchsorted(teams, float(match["blue"+str(1)]))
        b2 = np.searchsorted(teams, float(match["blue"+str(2)]))
        
        r0 = np.searchsorted(teams, float(match["red"+str(0)]))
        r1 = np.searchsorted(teams, float(match["red"+str(1)]))
        r2 = np.searchsorted(teams, float(match["red"+str(2)]))
        
def safe_div(a, b):
    if b != 0:
        return a/b
    else:
        return 0
    
    
def build_score_matrix(event_key, teams, matches):
    num_teams = len(teams)
    metrics = ["auto_score", "control_score", "endgame_score", "cell_score", "inner_goals", "high_goals", "low_goals", "extra_rp","fouls"]
    num_matches = len(matches)
    teams = np.array(teams)
    team_array = np.zeros([num_matches*2,num_teams])
    score_array = np.zeros([num_matches*2,len(metrics)])
    endgame_array = np.zeros([len(teams),2])
    i = 0
    for match in matches:
        if match["results"] == "Actual":
            metric_count = 0
            for metric in metrics:
                score_array[i][metric_count] = match["blue_" + metric]
                score_array[num_matches + i][metric_count] = match["red_" + metric]
                metric_count +=1
            
            for j in range(0,3):
                blue_index = np.searchsorted(teams, float(match["blue"+str(j)]))
                red_index = np.searchsorted(teams, float(match["red"+str(j)]))
                team_array[i][blue_index] = 1
                team_array[num_matches+i][red_index] = 1
                
                if match["blue_endgame_robot"+str(j+1)] == "Park":
                    endgame_array[blue_index][0] += 5
                    endgame_array[blue_index][1] +=1
                elif match["blue_endgame_robot"+str(j+1)] == "Hang":
                    endgame_array[blue_index][0] += 25
                    endgame_array[blue_index][1] +=1
                else:
                    endgame_array[blue_index][1] +=1
                if match["red_endgame_robot"+str(j+1)] == "Park":
                    endgame_array[red_index][0] += 5
                    endgame_array[red_index][1] +=1
                elif match["red_endgame_robot"+str(j+1)] == "Hang":
                    endgame_array[red_index][0] += 25
                    endgame_array[red_index][1] +=1
                else:
                    endgame_array[red_index][1] +=1
            i+=1        
    for i in range(0,len(endgame_array)):
        endgame_array[i][0] = safe_div(endgame_array[i][0],endgame_array[i][1])

    print(team_array, score_array, endgame_array)
    return team_array, score_array, endgame_array
    
def solve_matrix(matrix, solution):
    num_teams = matrix.shape[1]
    num_equations = matrix.shape[0]
    
    if num_equations > num_teams:
        X = np.zeros([matrix.shape[1],solution.shape[1]])
        for i in range(0,solution.shape[1]):
            X[:,i] = nnls(matrix,solution[:,i])[0]
        return X
    else:
        return np.linalg.lstsq(matrix,solution,rcond=None)[0]
        pass