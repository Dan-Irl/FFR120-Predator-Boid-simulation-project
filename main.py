# %%
from boid import Boid
from predator import Predator
from food import Food, food_spawn
from find_neighbours import findNeighbours, findClosestTarget, findTarget
import matplotlib.pyplot as plt
import numpy as np

#Parameters
generations = 10
dt = 0.1

# Boid parameters (Tuna)
N_boids = 20 # number of boids 
N_max_boids = 100 # maximum number of boids
r_CA = 8 # radius of cohesion and alignment
r_S = 5 # radius of separation
r_F = 5 # radius of food
r_FC = 10 # radius of food consumation REDUCE THIS
r_PA = 8 # radius of predator awareness
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
number_of_food = 5 


boids = [Boid(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt,L) for _ in range(N_boids)]
predators = [Predator(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_predator,r_S,L,dt) for _ in range(N_predators)]
food = [Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)) for _ in range(number_of_food)] 

#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
#render = ax.scatter([b.x for b in boids],[b.y for b in boids],[b.z for b in boids])


boid_history = [len(boids)]
predators_history = [len(predators)]
food_history = []

for gen in range(generations):
    boid_small_neighbours = findNeighbours(boids, r_S, L)   # find neighbours for separation
    boid_large_neighbours = findNeighbours(boids, r_CA, L)  # find neighbours for cohesion and alignment
    
    boid_food_location = findTarget(boids, food, r_F,L)     # find food for boids
    boid_food_to_consume = findTarget(boids,food, r_FC, L)    # check if food for boids is close enough to consume # HAVE TO CHANGE THIS
    
    boid_predator_neighbours = findNeighbours(predators, r_PA, L) # find predators for boids in their radius of awareness
    
    boid_targets = findClosestTarget(predators, boids, r_B, L)    # find closest boid targets for predators

    # 1. Update consumptions using consumption neighbour lists
    
    #Goes trough the food to be consumed list and removes the food from the food list and creates a new boid at the food position
    for consumed_food in boid_food_to_consume:
        if consumed_food is None:
            continue

        if consumed_food not in food:
            continue
        
        food.remove(consumed_food)
        food = food_spawn(1,food,L) #spawn new food 
        new_boid_cords = consumed_food.getPosition()
        
        # Create a new boid after it has eaten food at the food position
        if len(boids) < N_max_boids:
            boids.append(Boid(new_boid_cords[0],new_boid_cords[1],new_boid_cords[2],v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt,L))


    predatorSpawnLocations = []
    deadPredators = []
    for predator in predators:
        predator.checkRangeAndChase(boid_targets[predators.index(predator)])
        predator.updateVelocity()                                               # update velocity of predator
        predator.updatePosition()                                               # update position of predator
        
        if predator.getChasing() == True:
            if predator.checkCatch() and predator.chasing == True:                   # if predator catches boid
                predator.setChasing(False)
                predator.setChasedBoid(None)
                predator.feed()
                if predator.checkReproduce():
                    predatorSpawnPositions.append(predator.getPosition())
                    predator.setHealth(100)
                # predator.setResting(True)
                boids.remove(predator.getChasedBoid())
            predator.healthDecay()
            if predator.checkDead():
                deadPredators.append(predator)
    
    for pos in predatorSpawnLocations:
        predators.append(Predator(pos[0], pos[1], pos[2], v_predator, r_S, L, dt))  # spawn new predators
    for predator in deadPredators:
        predators.remove(predator)                                                  # remove dead predators

    # 2. Update positions of individuals that are left
    
    for boid in boids:
        boid.updateSmallFlock(boids, boid_small_neighbours[boids.index(boid)])    # update small flock 
        boid.updateLargeFlock(boids, boid_large_neighbours[boids.index(boid)])    # update large flock
        boid.updatePredators(predators, r_B, r_S)
        boid.updateFoodFlock(food, r_F)
        boid.updateVelocity(c_cohesion, c_separation, c_alignment, c_predators, c_food)
        boid.updatePosition()
        
        boid.foodlist = boid_food_location[boids.index(boid)]
        
    boid_history.append(len(boids))
    predators_history.append(len(predators))
    #food history

    if len(boids) < 1:
        break
    if len(predators) < 1:
        break  
    
#PLOTTING
