import googlemaps
from datetime import datetime
import time

import numpy as np
from joblib import Parallel,delayed
def distance(city1,city2,gmaps):
    now = datetime.now()
    directions_result = gmaps.directions(city1,
                                     city2,
                                     mode="driving",
                                     departure_time=now
                                    )
    return float(directions_result[0]['legs'][0]['distance']['value'])

def fill(team,team_num,team2_num,List,distance_mat):
    team2 = List[team2_num]
    if team_num != team2_num:
        distance_mat[team_num, team2_num] = distance(team, team2)
        time.sleep(0.1)
    else:
        distance_mat[team_num, team2_num] = 100000000000000

def distance_matrix_make(List,file_ext,APIkey):
    gmaps = googlemaps.Client(key=APIkey)
    print("Creating Distance Matrix")
    distance_mat = np.zeros((len(List),len(List)))
    for team_num in range(len(List)):
        team = List[team_num]
        print("Distance for "+team)
        #val = Parallel(n_jobs=2)(delayed(fill)(team,team_num,team2_num,List,distance_mat)for team2_num in range(len(List)))
        for team2_num in range(len(List)):
            team2 = List[team2_num]
            if team_num != team2_num:
                distance_mat[team_num,team2_num] = distance(team,team2,gmaps)
                time.sleep(0.1)
            else:
                distance_mat[team_num,team2_num] = 100000000000000



    np.savetxt('Distances'+file_ext+'.csv', distance_mat, delimiter=',')



