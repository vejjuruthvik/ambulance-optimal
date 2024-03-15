import math
import random
import numpy as np
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import folium
from operation_manager import block
from operation_manager import RouteManager
from operation_manager import Route
from operation_manager import population
from operation_manager import GA
from operation_manager import Ambulance
from operator import itemgetter
ox.config(log_console=True, use_cache=True)

def generateGrid(no_of_blocks, no_of_signals):
    rows = 60
    cols = 60

    # "0" represents Path is Clear
    for i in range(rows):
        for j in range(cols):
            RouteManager.addBlock(block(i * 60 + j, i, j, "0"))

    # "B" represents Path is Blocked
    for i in range(no_of_blocks):
        (RouteManager.getBlock(random.randint(0, RouteManager.numberOfBlocks() - 1))).setValue("B")

    # "S" represents Traffic Signal
    for i in range(no_of_signals):
        (RouteManager.getBlock(random.randint(0, RouteManager.numberOfBlocks() - 1))).setValue("S")


# print 2 best routes
def printPop(pop):
    for i in range(2):
        route = pop.getRoute(i)
        temp = []
        indexes = []

        for j in range(route.routeSize()):
            temp.append(route.getBlock(j).getValue())
            indexes.append(route.getBlock(j).getName())

        print("\nRoute_", i, ": ", temp)
        print("Indices of Route (in Grid)", indexes)
        print("Fitness: ", route.getFitness())
        print("Distance: ", route.getDistance())


# Get 2 Best Routes out of all calculated Routes of Population
def getRoutes(pop, noOfRoutes):
    routesPop = population(2, False)
    if pop.populationSize() >= noOfRoutes:
        for i in range(noOfRoutes):
            routesPop.saveRoute(i, pop.getRoute(i))
        return routesPop

    return None

def codeGenerator(starting_point, ending_point):
    locator = Nominatim(user_agent='mymap')
    start_location = locator.geocode(starting_point)
    end_location = locator.geocode(ending_point)
    start_loc_coords = (start_location.latitude, start_location.longitude)
    end_loc_coords = (end_location.latitude, end_location.longitude)
    
    code_dict = {'st_loc':start_location, 'ed_loc':end_location, 'st_coords':start_loc_coords, 'ed_coords':end_loc_coords}
    print(code_dict)
    return code_dict


def start_Genetic_Algorithm(st, goal):
    startBlock = st
    destBlock = goal

    # to increase accuracy, increase "iterations"
    chromosomeSize = 20
    iterations = 10

    pop = population(20, True, startBlock, destBlock, chromosomeSize)
    print("Initial distance (Before Genetic Algorithm): ", pop.getFittest().getDistance())

    pop = GA.evolvePopulation(pop)

    for i in range(iterations):
        pop = GA.evolvePopulation(pop)

    return pop


# schedule ambulances based on Severity of Patients
def scheduling_ambulance(amb, calls):
    calls = sorted(calls, key=itemgetter(1), reverse=True)

    for i in range(amb.__len__()):
        if amb[i].getisFree() is True:
            amb[i].setStart(calls[i][0][0])
            amb[i].setEnd(calls[i][0][1])
            amb[i].setisFree(False)
            print("\nAmbulance :", i)
            y = start_Genetic_Algorithm(amb[i].getStart(), amb[i].getEnd())
            amb[i].setAllRoutes(getRoutes(y, 2))



