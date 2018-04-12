import csv
import string
import pandas as pd
f = open('distances_latlon.csv', 'r')
reader = csv.reader(f)
cities_list = list(reader)
f.close()

from mapsplotlib import mapsplot as mplt



mplt.register_api_key('AIzaSyC23WZ06xZau9Gw2R_ulYm6f0L5uxLdAeM')


cities_lat = []
cities_lon = []
color = []
size = []
marker_list = []
Upper = list(string.ascii_uppercase)
digits = list(string.digits)
markers = Upper+digits
for i in range(len(cities_list)):
    cities_lat.append(float(cities_list[i][0]))
    cities_lon.append(float(cities_list[i][1]))
    color.append('blue')
    size.append('medium')
    marker_list.append(markers[i])

df = pd.DataFrame.from_items([('latitude', cities_lat), ('longitude', cities_lon), ('color',color),('size',size),('label', marker_list)])


mplt.plot_markers(df)




