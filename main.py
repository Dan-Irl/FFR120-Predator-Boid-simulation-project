# %%
from boid import Boid
from predator import Predator
from food import Food, food_spawn
from find_neighbours import findNeighbours, findClosestTarget, findTarget, findAllTargets
import matplotlib.pyplot as plt
import numpy as np

#Parameters
generations = 1000
dt = 1

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
N_predators = 5 # number of predators
r_B = 10 # radius of boid sensing
r_S = 2 # radius of separation
v_predator = 2 # velocity
reproduction_cutoff = 150 # health points required to reproduce
healthGain = 50

#food parameters
nFood = 10           # number of food at start
# foodSpawnRate = 1   # number of food that spawn per generation
foodSpawnRate = 0.1  # spawns one food every 1/foodSpawnRate generations  

boids = [Boid(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt,L) for _ in range(N_boids)]
predators = [Predator(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_predator,r_S,L,dt) for _ in range(N_predators)]
foods = [Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)) for _ in range(nFood)] 

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
render = ax.scatter([b.x for b in boids],[b.y for b in boids],[b.z for b in boids])
plt.show()


boid_history = [len(boids)]
predators_history = [len(predators)]
food_history = []

all_boids_dead = False
for gen in np.arange(0, generations+10, 10):
    print("Generation: ", gen)
    print("Number of boids: ", len(boids))
    print("Number of predators: ", len(predators))
    print("Number of food: ", len(foods))
    print("====================================")
    
    # 1. Predators search for boids, chase them and eat them  
    boid_targets = findClosestTarget(predators, boids, r_B, L)    # find closest boid targets for predators

    predatorSpawnLocations = []
    deadPredators = []
    
    # proposal for predator logic
    # 1. check if predator is dead and simply remove it from the list instead of appending to remove list
        # Answer: From my experience in the past, it is better to remove the dead predators from the list after the loop is done. 
        # This is because if you remove them while looping, the loop will skip the next predator in the list. 
        # This is because the list is shortened by one element. 
        # (LMAO this comment is from Github Copilot but says what I wanted to say) 
    # 2. Check if predator is chasing and has caught a boid
        # Answer: My thinking is a predator moves at the start of a gen, and sees if it can catch a boid before the boid moves.
    # 3. Update predator behaviour
    # 4. Append predator directly to predator list instead of to predator spawn location list
        # See Answer to 1.
    # 5. Thats all i think? it would simplyfy the code a lot imo
    
    for predator in predators:
        predator.checkRangeAndChase(boid_targets[predators.index(predator)])
        predator.updateVelocity()                                               # update velocity of predator
        predator.updatePosition()                                               # update position of predator
        
        if predator.chasing == True:                                            # if predator is chasing a boid
            if predator.checkIfCaught():                                           # if predator catches boid
                print("Predator caught boid")
                predator.feed(healthGain)
                boids.remove(predator.getChasedBoid()) if predator.getChasedBoid() in boids else None
                if len(boids) < 1:
                    all_boids_dead = True
                    break

                if predator.checkReproduce(reproduction_cutoff):                                   # if predator is ready to reproduce 
                    predatorSpawnLocations.append(predator.getPosition())
                    predator.health = 100
                # predator.setResting(True)
                predator.chasing = False
                predator.chasedBoid = None
            predator.healthDecay()
            if predator.health < 1:
                deadPredators.append(predator)

    if all_boids_dead:
        print("All boids are dead")
        break

    # 2. new predators spawn and dead predators are removed
    for pos in predatorSpawnLocations:
        predators.append(Predator(pos[0], pos[1], pos[2], v_predator, r_S, L, dt))  # spawn new predators
    for predator in deadPredators:
        predators.remove(predator)                                                  # remove dead predators

    if len(predators) < 1:
        print("All predators are dead")
        break
    
    # 3. The boids that are left search for food and predators
    boid_predator_neighbours = findAllTargets(boids, predators, r_PA, L) # find predators for boids in their radius of awareness
    # boid_food_location = findAllTargets(boids, foods, r_F, L)            # finds all food in range for boids
    boid_food_targets = findClosestTarget(boids, foods, r_F, L)            # finds closest food for boids

    # 4. The boids that are left search for other boids and update their velocity and position
    boid_small_neighbours = findNeighbours(boids, r_S, L)   # find neighbours for separation
    boid_large_neighbours = findNeighbours(boids, r_CA, L)  # find neighbours for cohesion and alignment
    
    for boid in boids:
        # boid.updateSmallFlock(boids, boid_small_neighbours[boids.index(boid)])    # update small flock 
        # boid.updateLargeFlock(boids, boid_large_neighbours[boids.index(boid)])    # update large flock
        boid.updateSmallFlock(boids, boid_small_neighbours)                         # update small flock
        boid.updateLargeFlock(boids, boid_large_neighbours)                         # update large flock

        boid.updatePredators(boid_predator_neighbours[boids.index(boid)])           # update predator list

    # Alternative 1: All foods in range
        # boid.updateFoodList(boid_food_location[boids.index(boid)])                # update food list
    # Alternative 2: Closest food
        boid.closestFood = boid_food_targets[boids.index(boid)]                     # update closest food

        # boid.updateVelocity(c_cohesion, c_separation, c_alignment, c_predators, c_food)
        boid.updateVelocity()
        boid.updatePosition()
                
    # 5. Boids eat food and reproduce
    food_boid_neighbours = findClosestTarget(foods, boids, r_FC, L)                                # find closest boid in range to eat food
    consumed_foods = [foods[i] for i in range(len(foods)) if food_boid_neighbours[i] is not None]  # food is added if there is a boid in range to eat it
    for consumed_food in consumed_foods:
        print("Boid ate food")
        # Create a copy of a boid after it has eaten food
        new_boid_coords = consumed_food.getPosition()
        foods.remove(consumed_food) if consumed_food in foods else None 
        if len(boids) < N_max_boids:                   
            boids.append(Boid(new_boid_coords[0],new_boid_coords[1],new_boid_coords[2],v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt,L))
        
    # 6. New food spawns
    # for i in range(foodSpawnRate):
    #     foods.append(Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)))
    if gen % (1/foodSpawnRate) == 0:                                                                # spawn new food every 1/foodSpawnRate generations
        foods.append(Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)))

    # Update history
    boid_history.append(len(boids))
    predators_history.append(len(predators))
    # food history

    if len(boids) < 1:
        print("All boids are dead")
        break
    if len(predators) < 1:
        print("All predators are dead")
        break  
    
#PLOTTING 