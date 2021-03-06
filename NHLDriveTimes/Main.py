from Map import map
from CreateDistanceMatrix import distance_matrix_make
from CalculateShortestRoute import shortest_route_calculation
from Time import calculate_time
#--------------------INPUT PARAMETERS-------------------#
create_dist_mat = False  # Create Distance Matrix
calc_shortest = False # Calculate Distances
map_it = False # Pretty Map
calc_time = True # Total Drive time for shortest route
file_ext = 'nhl'
api_key = 'APIKEY'
#-------------------------------------------------------#
#--------------List of Locations------------------------#
Atlantic_div = ['Boston, MA','Buffalo, NY','Detroit, MI','Miami, FL','Montreal, QC, Canada','Ottawa, ON, Canada','Tampa, FL','Toronto, ON, Canada']
Metro_div = ['Raleigh, NC','Columbus, OH','East Rutherford, NJ','New York, NY','Philadelphia, PA','Pittsburgh, PA','Washington D.C.']
Central_div = ['Chicago, IL','Denver, CO','Dallas, TX','Minneapolis, MN','Nashville, TN','St. Louis, MO','Winnipeg, MB, Canada']
Pacific_div = ['Anaheim, CA','Glendale, AZ','Calgary, AB, Canada','Edmonton, AB','Los Angeles, CA','San Jose, CA','Vancouver, BC, Canada','Paradise, NV']
NHLTeams = Atlantic_div+Metro_div+Central_div+Pacific_div
#-------------------------------------------------------#


def main():
    if create_dist_mat == True:
        distance_matrix_make(NHLTeams,file_ext,api_key)
    if calc_shortest == True:
        shortest_route_calculation(NHLTeams,file_ext)
    if map_it == True:
        map(file_ext)
    if calc_time == True:
        calculate_time(file_ext,api_key)

main()

