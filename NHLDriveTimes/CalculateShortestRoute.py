import numpy as np
from geopy.geocoders import Nominatim
import csv

Atlantic_div = ['Boston, MA','Buffalo, NY','Detroit, MI','Miami, FL','Montreal, QC, Canada','Tampa, FL','Toronto, ON, Canada']
Metro_div = ['Raleigh, NC','Columbus, OH','East Rutherford, NJ','New York, NY','Philadelphia, PA','Pittsburgh, PA','Washington D.C.']
Central_div = ['Chicago, IL','Denver, CO','Dallas, TX','Minneapolis, MN','Nashville, TN','St. Louis, MO','Winnipeg, MB, Canada']
Pacific_div = ['Anaheim, CA','Glendale, AZ','Calgary, AB, Canada','Edmonton, AB','Los Angeles, CA','San Jose, CA','Vancouver, BC, Canada','Paradise, NV']
NHLTeams = Atlantic_div+Metro_div+Central_div+Pacific_div

distance_matrix = np.genfromtxt('Distances.csv', delimiter=',')
num_to_team = dict()
team_to_num = dict()
for i in range(len(NHLTeams)):
    num_to_team[i] = NHLTeams[i]
    team_to_num[NHLTeams[i]] = i
shortest_per_team = dict()
def mintonext(distance_mat,NHLTeams):
    min_to_next_ind = np.argwhere(distance_mat == np.min(distance_mat))[0][0]
    min_to_next_team = NHLTeams[min_to_next_ind]
    distance_Traveled = distance_mat[min_to_next_ind]
    return min_to_next_ind,min_to_next_team,distance_Traveled

for team_num in range(len(NHLTeams)):
    team = NHLTeams[team_num]
    total_dist = 0
    distances = distance_matrix[team_num][:]
    distances_new = distances
    teams_visited = []
    teams_visited.append(team)
    while len(teams_visited) < len(distance_matrix):
        next_ind, next_team, min_dist = mintonext(distances_new, NHLTeams)
        if next_team not in teams_visited:
            teams_visited.append(next_team)
            team = next_team
            team_number_original = team_to_num[team]
            team_num = next_ind
            total_dist += min_dist
            NHLTeams = Atlantic_div+Metro_div+Central_div+Pacific_div#reset
            distances_new = distance_matrix[team_number_original][:]
        else:
            NHLTeams = NHLTeams[:next_ind]+NHLTeams[next_ind+1:]
            distances_new = np.delete(distances_new, next_ind)#, axis=1)
    dist_teams = dict()
    dist_teams[total_dist] = teams_visited
    shortest_per_team[teams_visited[0]] = dist_teams

distances_of_shortest = 1000000000000000
ind_of_shortest = 0
for i in range(len(NHLTeams)):
    for key in shortest_per_team[NHLTeams[i]]:
        dist_of_short = key
    if dist_of_short < distances_of_shortest:
        distances_of_shortest = dist_of_short
        ind_of_shortest = i
    else:
        pass


shortest_list = shortest_per_team[NHLTeams[ind_of_shortest]][distances_of_shortest]

lat_lon = []
geolocator = Nominatim()
location = geolocator.geocode('Los Angeles, CA')
def getlatlon(loc):
    location = geolocator.geocode(loc)
    return (location.latitude,location.longitude)

for city in shortest_list:
    lat_lon.append(getlatlon(city))

file = open('shortest.txt','w')

filecsv = open('distances.csv','w')
filecsv2 = open('distances_latlon.csv','w')

writer = csv.writer(filecsv)
count = 0
for item in shortest_list:
    file.write(item+"\n")
    filecsv2.write(str(lat_lon[count][0])+","+str(lat_lon[count][1])+"\n")
    count += 1
file.close()
writer.writerow(shortest_list)
filecsv.close()
filecsv2.close()