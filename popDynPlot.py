# Test file for plotting
import matplotlib.pyplot as plt
import numpy as np
# Test variables
generations = 100
plotTrue = 1

# From main take generations argument

Timesteps = list(range(generations))
boidPopOverTime = []

for i in range(generations):
    boidPopOverTime.append(2*i)

# len(Boids)
# len(Predators)
# len(Food)
if plotTrue==1:
    #plt.xlabel('$Timestep$')

    plt.plot(Timesteps,boidPopOverTime)
    plt.show()