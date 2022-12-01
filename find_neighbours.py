#function that calculates the closest neighbours of each indivial. 
# Assumes that the indivial class has a .getPosition() method that returns a tuple of the x and y coordinates of the individual. 
# The range is the distance that is considered to be a neighbour. 
# The boundingBox is the size of the area that the individuals are in. This is used to wrap the individuals around the edges of the area. 
# The function returns a list of lists. Each list contains the indices of the individuals that are neighbours of the individual with the same index as the list.
# List if neighbours includes the individual itself.
from scipy.spatial import KDTree
import numpy as np

def findNeighbours(individuals:list,range:int,boundingBox:int) -> list:
    """Finds all neighbours for each individual given a range."""
    positions = np.array([individual.getPosition() for individual in individuals])
    tree = KDTree(positions,boxsize=boundingBox)
    return tree.query_ball_point(positions, range)

# Function that finds bad neighbours

def findTarget(Individuals:list,Targets:list,range:int,boundingBox:int) -> list:
    """Finds the closest target for each individual given a list of targets and a range."""
    positions = np.array([individual.getPosition() for individual in Individuals])
    targets = np.array([target.getPosition() for target in Targets])
    tree = KDTree(targets,boxsize=boundingBox)

    # return [Targets[index[0]] for index in tree.query_ball_point(positions, range)]
    # Alternative, handling the case where there are no targets in range //Jesper
    targetList = []
    for index in tree.query_ball_point(positions, range):
        if index != []:
            targetList.append(Targets[index[0]])
        else:
            targetList.append(None)
    return targetList