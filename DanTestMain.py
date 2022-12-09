# %%
from boid import Boid
from predator import Predator
from food import Food, food_spawn
from find_neighbours import findNeighbours, findClosestTarget, findTarget, findAllTargets
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

#Parameters
generations = 50000
dt = 1
timeCounter = 0

# Boid parameters (Tuna)
N_boids = 10 # number of boids 
N_max_boids = 200 # maximum number of boids
r_CA = 8 # radius of cohesion and alignment
r_S = 5 # radius of separation
r_F = 15 # radius of food sensing
r_FC = 3 # radius of food consumation REDUCE THIS
r_PA = 8 # radius of predator awareness
v_boid = 1 # velocity
L = 300 # length of the simulation area
c_cohesion = 1.5 # cohesion coefficient
c_alignment = 1 # alignment coefficient
c_separation = 2 # separation coefficient
c_food = 1000 # food search coefficient
c_predators = 1 # predator avoidance coefficient

# predator parameters (Tiger shark)
N_predators = 10 # number of predators
r_B = 10 # radius of boid sensing
r_S = 2 # radius of separation
v_predator = 3 # velocity
reproduction_cutoff = 110  # health points required to reproduce
healthGain = 10            # health points gained from eating a boid

#food parameters
nFood = 5           # number of food at start
# foodSpawnRate = 1   # number of food that spawn per generation
foodSpawnRate = 0.01  # spawns one food every 1/foodSpawnRate generations  

boids = [Boid(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_boid,c_cohesion,c_alignment,c_separation,c_predators,c_food,dt,L) for _ in range(N_boids)]
predators = [Predator(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L),v_predator,r_S,L,dt) for _ in range(N_predators)]
foods = [Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)) for _ in range(nFood)] 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(0, L)
ax.set_ylim3d(0, L)
ax.set_zlim3d(0, L)



fig.tight_layout()
fig.set_facecolor('#D6FFFF')

boid_history = [len(boids)]
predators_history = [len(predators)]
food_history = [len(foods)]

all_boids_dead = False
for gen in np.arange(0, generations+100, 100):
    
    # 1. Predators search for boids, chase them and eat them  
    boid_targets = findClosestTarget(predators, boids, r_B, L)    # find closest boid targets for predators

    predatorSpawnLocations = []
    deadPredators = []
    for predator in predators:
        predator.checkRangeAndChase(boid_targets[predators.index(predator)])
        predator.updateVelocity()                                               # update velocity of predator
        predator.updatePosition()                                               # update position of predator
        
        if predator.chasing == True:                                            # if predator is chasing a boid
            if predator.checkIfCaught():                                        # if predator catches boid
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
    if gen*dt % (1/foodSpawnRate) == 0:                                                                # spawn new food every 1/foodSpawnRate generations
        foods.append(Food(np.random.uniform(L),np.random.uniform(L),np.random.uniform(L)))

    # Update history
    boid_history.append(len(boids))
    predators_history.append(len(predators))
    food_history.append(len(foods))
    # food history
    # Counter update to allow plotting with or without break
    timeCounter += 1
    if len(boids) < 1:
        print("All boids are dead")
        break
    if len(predators) < 1:
        print("All predators are dead")
        break  
    
    #PLotting
    ax.cla()  # Clear the previous frame
    ax.scatter([b.x for b in boids],[b.y for b in boids],[b.z for b in boids],color='blue', marker='o')
    ax.scatter([p.x for p in predators],[p.y for p in predators],[p.z for p in predators],color='red', marker='D', s=100)
    ax.scatter([f.x for f in foods],[f.y for f in foods],[f.z for f in foods],color='green',marker='P')
    ax.set_facecolor('#D6FFFF')
    ax.set_xlim3d(0, L)
    ax.set_ylim3d(0, L)
    ax.set_zlim3d(0, L)
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0)) 
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.set_xticks([])                               
    ax.set_yticks([])                               
    ax.set_zticks([]) 
    # Add a text label with the particle count
    label1 = fig.text(0.05,0.05, f"Particle count: {len(boids)}, Predator count: {len(predators)}, Food count: {len(foods)}", )
    
    # Pause for a fixed interval
    plt.pause(0.04)
    label1.remove()  # Remove the previous label

plt.show()

#PLOTTING for graphs (PopDyn over simulation)
doPlot = False
doPlot = True
if doPlot:
    Timesteps = list(range(timeCounter+1))
    # len for Debugging
    #print(len(Timesteps))
    #print(len(boid_history))
    #print(len(predators_history))
    plt.figure()
    plt.plot(Timesteps, boid_history, color='darkturquoise', label='Boids' )
    plt.plot(Timesteps, predators_history, color='coral', label='Predators' )
    plt.plot(Timesteps, food_history, color='palegreen', label='Food' ) # No Foodhistory yet
    plt.xlabel('$Timestep$')
    plt.ylabel("Numbers")
    plt.title("Populations of boids, predators and food over time")
    plt.legend()
    plt.show()