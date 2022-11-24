import random 
import numpy as np 

# Class food
class Food():
    def __init__(self, x, y, z, L):
        self.x = x
        self.y = y
        self.z = z
        self.L = L
   
# Function for food spawning
def food_spawn(self, number_of_food, food_list):
    for i in range(number_of_food):
        x = np.random.random() * self.L
        y = np.random.random() * self.L
        z = np.random.random() * self.L
        food_list.append(Food(x,y,z))
    return food_list
