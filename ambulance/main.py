#from helpers import Map, load_map_10, load_map_40, show_map
import math
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium
import webbrowser
from support import codeGenerator
import argparse
from operation_manager import RouteManager
from operation_manager import Route
from utils import Rollouts


def route_input():
    starting_point = input('Enter Source: ')
    ending_point = input('Enter Destination: ')
    print("Source: {0}\nDestination: {1}".format(starting_point, ending_point))
    return [starting_point, ending_point]

if __name__=='__main__':
    
    ox.config(log_console=True, use_cache=True)
    rm = RouteManager()
    mp = Route()
    rol = Rollouts()
    
    ri_op = route_input()
    latlng_codes = codeGenerator(ri_op[0], ri_op[1])
    start_loc_coords = latlng_codes['st_coords']
    end_loc_coords = latlng_codes['ed_coords']
    
    mode = 'drive'
    optimizer = 'time'
    
    map_dict = rm.get_nodes(start_loc_coords, end_loc_coords)
    route_map = mp.generateMap(map_dict)
    
    rs_graph = rol.add_markers(route_map, latlng_codes)
    
    rs_graph.save('map.html')
    
    file_path = 'map.html'
    webbrowser.open(file_path, new=0)