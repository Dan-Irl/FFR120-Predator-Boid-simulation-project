#function that calculates the closest neighbours of each indivial. 
# Assumes that the indivial class has a .getPosition() method that returns a tuple of the x and y coordinates of the individual. 
# The range is the distance that is considered to be a neighbour. 
# The boundingBox is the size of the area that the individuals are in. This is used to wrap the individuals around the edges of the area. 
# The function returns a list of lists. Each list contains the indices of the individuals that are neighbours of the individual with the same index as the list.
# List if neighbours includes the individual itself.
from scipy.spatial import cKDTree
import numpy as np

def findNeighbours(individuals:list,range:int,boundingBox:int) -> list:
    positions = np.array([individual.getPosition() for individual in individuals])
    tree = cKDTree(positions,boxsize=boundingBox)
    return tree.query_ball_point(positions, range)