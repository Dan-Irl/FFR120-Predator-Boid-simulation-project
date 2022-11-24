from boid import Boid
from predator import Predator
from food import Food, food_spawn
import numpy as np

#Parameters
generations = 1000

# Boid parameters (Tuna)
N_boids = 50 # number of boids 
r_CA = 5 # radius of cohesion and alignment
r_S = 5 # radius of separation
r_F = 5 # radius of food
v_boid = 2 # velocity
L = 100 # length of the simulation area
c_cohesion = 1 # cohesion coefficient

# predator parameters (Tiger shark)
N_predators = 1 # number of predators
r_B = 10 # radius of boid sensing
r_S = 2 # radius of separation
v_predator = 2 # velocity

#food parameters
number_of_food = 2


boids = [Boid for _ in range(N_boids)]
predators = [Predator for _ in range(N_predators)]
food = [Food for _ in range(N_predators)]


boid_history = [len(boids)]
predators_history = [len(predators)]
food_history = []

for gen in range(Generations):
    boid_small_neighbours = findNeighbours(boids, r, L)
    boid_large_neighbours = findNeighbours(boids, r, L)
    
    
    
    boid_food_location = findNeighbours(boids, r, L)
    boid_food_consumed = findNeighbours(boids, r, L)
    boid_predator_neighbours = findNeighbours(boids, r, L)
    predator_boid_neighbours = findNeighbours(predators, r, L)
    
    
    # 1. Update consumptions using consumption neighbour lists
    # 2. Update positions of individuals that are left
    

    
    for boid in boids:
        boid.updateSmallFlock(boids, r_CA, r_S, r_F)
        boid.updateLargeFlock(boids, r_CA, r_S, r_F)
        boid.updatePredators(predators, r_B, r_S)
        boid.updateFoodFlock(food, r_F)
        boid.updateVelocity(c_cohesion, c_separation, c_alignment, c_predators, c_food)
        boid.updatePosition()

    for predator in predators:
        predator.updateSmallFlock(boids, r_B, r_S)
        predator.updatePosition()

    for food in food:
        #Check if food is eaten and add boid to its location
        food_list = food_spawn(number_of_food,food_list,L)
        food.updatePosition()
        
    boid_history.append(len(boids))
    predators_history.append(len(predators))
    #food history

    if len(boids) < 1:
        break
    if len(predators) < 1:
        break
    
    
    
#PLOTTING
