from boid import Boid
from predator import Predator
from food import Food, food_spawn
from find_neighbours import findNeighbours
import numpy as np

#Parameters
generations = 10
dt = 0.1

# Boid parameters (Tuna)
N_boids = 50 # number of boids 
r_CA = 8 # radius of cohesion and alignment
r_S = 5 # radius of separation
r_F = 5 # radius of food
r_FC = 1 # radius of food consumation
r_PA = 10 # radius of pradtor awareness
v_boid = 2 # velocity
L = 100 # length of the simulation area
c_cohesion = 1 # cohesion coefficient
c_alignment = 1 # alignment coefficient
c_separation = 2 # separation coefficient
c_food = 1 # food search coefficient
c_predators = 1 # predator avoidance coefficient

# predator parameters (Tiger shark)
N_predators = 1 # number of predators
r_B = 10 # radius of boid sensing
r_S = 2 # radius of separation
v_predator = 2 # velocity

#food parameters
number_of_food = 2


boids = [Boid(np.random.random(L),np.random.random(L),np.random.random(L),v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt) for _ in range(N_boids)]
predators = [Predator for _ in range(N_predators)]
food = [Food for _ in range(N_predators)]


boid_history = [len(boids)]
predators_history = [len(predators)]
food_history = []

for gen in range(generations):
    boid_small_neighbours = findNeighbours(boids, r_S, L)
    boid_large_neighbours = findNeighbours(boids, r_CA, L)
    
    
    boid_food_location = findNeighbours(boids, r_F, L)
    boid_food_consumed = findNeighbours(boids, r_FC, L)
    boid_predator_neighbours = findNeighbours(boids, r_PA, L)
    predator_boid_neighbours = findNeighbours(predators, r_B, L)
    
    
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
        food = food_spawn(number_of_food,food,L)
        food.updatePosition()

    boid_history.append(len(boids))
    predators_history.append(len(predators))
    #food history

    if len(boids) < 1:
        break
    if len(predators) < 1:
        break
    
    
    
#PLOTTING
