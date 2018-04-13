from Map import map
from CreateDistanceMatrix import distance_matrix_make
from CalculateShortestRoute import shortest_route_calculation
from Time import calculate_time
create_dist_mat = False  #only if not already made
calc_shortest = False
map_it = False
calc_time = True
file_ext = 'nhl'


Atlantic_div = ['Boston, MA','Buffalo, NY','Detroit, MI','Miami, FL','Montreal, QC, Canada','Ottawa, ON, Canada','Tampa, FL','Toronto, ON, Canada']
Metro_div = ['Raleigh, NC','Columbus, OH','East Rutherford, NJ','New York, NY','Philadelphia, PA','Pittsburgh, PA','Washington D.C.']
Central_div = ['Chicago, IL','Denver, CO','Dallas, TX','Minneapolis, MN','Nashville, TN','St. Louis, MO','Winnipeg, MB, Canada']
Pacific_div = ['Anaheim, CA','Glendale, AZ','Calgary, AB, Canada','Edmonton, AB','Los Angeles, CA','San Jose, CA','Vancouver, BC, Canada','Paradise, NV']
NHLTeams = Atlantic_div+Metro_div+Central_div+Pacific_div



def main():
    if create_dist_mat == True:
        distance_matrix_make(NHLTeams,file_ext)
    if calc_shortest == True:
        shortest_route_calculation(NHLTeams,file_ext)
    if map_it == True:
        map(file_ext)
    if calc_time == True:
        calculate_time(file_ext)

main()

