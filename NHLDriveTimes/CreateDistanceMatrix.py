import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyC23WZ06xZau9Gw2R_ulYm6f0L5uxLdAeM')
import numpy as np

def distance(city1,city2):
    now = datetime.now()
    directions_result = gmaps.directions(city1,
                                     city2,
                                     mode="driving",
                                     departure_time=now
                                    )
    return float(directions_result[0]['legs'][0]['distance']['value'])

Atlantic_div = ['Boston, MA','Buffalo, NY','Detroit, MI','Miami, FL','Montreal, QC, Canada','Ottawa, ON, Canada','Tampa, FL','Toronto, ON, Canada']
Metro_div = ['Raleigh, NC','Columbus, OH','East Rutherford, NJ','New York, NY','Philadelphia, PA','Pittsburgh, PA','Washington D.C.']
Central_div = ['Chicago, IL','Denver, CO','Dallas, TX','Minneapolis, MN','Nashville, TN','St. Louis, MO','Winnipeg, MB, Canada']
Pacific_div = ['Anaheim, CA','Glendale, AZ','Calgary, AB, Canada','Edmonton, AB','Los Angeles, CA','San Jose, CA','Vancouver, BC, Canada','Paradise, NV']
NHLTeams = Atlantic_div+Metro_div+Central_div+Pacific_div
distance_mat = np.zeros((len(NHLTeams),len(NHLTeams)))
for team_num in range(len(NHLTeams)):
    team = NHLTeams[team_num]
    for team2_num in range(len(NHLTeams)):
        team2 = NHLTeams[team2_num]
        if team_num != team2_num:
            distance_mat[team_num,team2_num] = distance(team,team2)
        else:
            distance_mat[team_num,team2_num] = 100000000000000


np.savetxt('Distances.csv', distance_mat, delimiter=',')



