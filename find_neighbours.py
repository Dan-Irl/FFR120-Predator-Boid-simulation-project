#function that calculates the closest neighbours of each indivial. 
# Assumes that the indivial class has a .getPosition() method that returns a tuple of the x and y coordinates of the individual. 
# The radius is the distance that is considered to be a neighbour. 
# The boundingBox is the size of the area that the individuals are in. This is used to wrap the individuals around the edges of the area. 
# The function returns a list of lists. Each list contains the indices of the individuals that are neighbours of the individual with the same index as the list.
# List if neighbours includes the individual itself.
from scipy.spatial import KDTree
import numpy as np

def findNeighbours(individuals:list,radius:int,boundingBox:int) -> list:
    """Finds all neighbours for each individual given a radius."""
    positions = np.array([individual.getPosition() for individual in individuals])
    tree = KDTree(positions,boxsize=boundingBox)
    return tree.query_ball_point(positions, radius)

# Function that finds bad neighbours

def findTarget(Individuals:list,Targets:list,radius:int,boundingBox:int) -> list:
    """Finds the closest target for each individual given a list of targets and a radius."""
    positions = np.array([individual.getPosition() for individual in Individuals])
    targets = np.array([target.getPosition() for target in Targets])
    tree = KDTree(targets,boxsize=boundingBox)

    # return [Targets[index[0]] for index in tree.query_ball_point(positions, radius)]
    # Alternative, handling the case where there are no targets in radius //Jesper
    targetList = []
    for index in tree.query_ball_point(positions, radius):
        if index != []:
            targetList.append(Targets[index[0]])
        else:
            targetList.append([])
     
    return targetList

def findAllTargets(Individuals:list,Targets:list,radius:int,boundingBox:int) -> list:
    """Finds all targets for each individual given a list of targets and a radius."""
    positions = np.array([individual.getPosition() for individual in Individuals])
    targets = np.array([target.getPosition() for target in Targets])
    tree = KDTree(targets,boxsize=boundingBox)

    targetList = []
    for index in tree.query_ball_point(positions, radius):
        if len(index) > 0:
            targetList.append([Targets[i] for i in index])
        else:
            targetList.append([])
    return targetList

# Function that finds the closest target of each individual
def findClosestTarget(Individuals:list,Targets:list,radius:int,boundingBox:int) -> list:
    """Finds the closest target for each individual given a list of targets and a radius."""
    positions = np.array([individual.getPosition() for individual in Individuals])
    targets = np.array([target.getPosition() for target in Targets])
    tree = KDTree(targets, boxsize=boundingBox)
    
    distances, indices = tree.query(positions, k=1, distance_upper_bound=radius)

    targetList = []
    for i in range(len(indices)):
        if distances[i] != np.inf:
            targetList.append(Targets[indices[i]])
        else:
            targetList.append(None)
    
    return targetList