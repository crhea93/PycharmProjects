import numpy as np
from geopy.geocoders import Nominatim
import csv
from joblib import Parallel,delayed


def mintonext(distance_mat,List):
    min_to_next_ind = np.argwhere(distance_mat == np.min(distance_mat))[0][0]
    min_to_next_team = List[min_to_next_ind]
    distance_Traveled = distance_mat[min_to_next_ind]
    return min_to_next_ind,min_to_next_team,distance_Traveled

def getlatlon(loc):
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    return (location.latitude,location.longitude)


def shortest_route_calculation(List,file_ext):
    print("Calculating Shortest Route")
    List_original = List
    distance_matrix = np.genfromtxt('Distances'+file_ext+'.csv', delimiter=',')
    num_to_team = dict()
    team_to_num = dict()
    for i in range(len(List)):
        num_to_team[i] = List[i]
        team_to_num[List[i]] = i
    shortest_per_team = dict()
    for team_num in range(len(List)):
        team = List[team_num]
        total_dist = 0
        distances = distance_matrix[team_num][:]
        distances_new = distances
        teams_visited = []
        teams_visited.append(team)
        while len(teams_visited) < len(distances):
            next_ind, next_team, min_dist = mintonext(distances_new, List)
            if next_team not in teams_visited:
                teams_visited.append(next_team)
                team = next_team
                team_number_original = team_to_num[team]
                #team_num = next_ind
                total_dist += min_dist
                List = List_original#reset
                distances_new = distance_matrix[team_number_original][:]
            else:
                List = List[:next_ind]+List[next_ind+1:]
                distances_new = np.delete(distances_new, next_ind)#, axis=1)
        dist_teams = dict()
        dist_teams[total_dist] = teams_visited
        shortest_per_team[teams_visited[0]] = dist_teams

    distances_of_shortest = 1000000000000000
    ind_of_shortest = 0
    for i in range(len(List)):
        for key in shortest_per_team[List[i]]:
            dist_of_short = key
        if dist_of_short < distances_of_shortest:
            distances_of_shortest = dist_of_short
            ind_of_shortest = i
        else:
            pass


    shortest_list = shortest_per_team[List[ind_of_shortest]][distances_of_shortest]

    lat_lon = []


    for city in shortest_list:
        lat_lon.append(getlatlon(city))

    file = open('shortest'+file_ext+'.txt', 'w')

    filecsv = open('distances'+file_ext+'.csv', 'w')
    filecsv2 = open('distances_latlon'+file_ext+'.csv', 'w')

    writer = csv.writer(filecsv)
    count = 0
    for item in shortest_list:
        file.write(item + "\n")
        filecsv2.write(str(lat_lon[count][0]) + "," + str(lat_lon[count][1]) + "\n")
        count += 1
    file.close()
    writer.writerow(shortest_list)
    filecsv.close()
    filecsv2.close()


