import googlemaps
from datetime import datetime


def time(city1,city2,gmaps):
    now = datetime.now()
    directions_result = gmaps.directions(city1,
                                     city2,
                                     mode="driving",
                                     departure_time=now
                                    )
    return float(directions_result[0]['legs'][0]['duration']['value'])

def calculate_time(file_ext,api_key):
    gmaps = googlemaps.Client(key=api_key)
    cities_list = []
    f = open('shortest'+file_ext+'.txt')
    for line in f:
        cities_list.append(line)
    total_time = 0
    for city in range(len(cities_list)-1):
        city1 = cities_list[city]
        city2 = cities_list[city+1]
        total_time += time(city1,city2,gmaps)
    print("Total Drive Time is "+str(round(total_time/60/60))+" hours")