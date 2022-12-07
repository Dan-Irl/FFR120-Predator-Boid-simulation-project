import random 
import numpy as np 

# Class food
class Food():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def getPosition(self):
        return (self.x, self.y, self.z)
        
# Function for food spawning
def food_spawn(self, number_of_food, food_list, L):
    for i in range(number_of_food):
        x = np.random.random() * L
        y = np.random.random() * L
        z = np.random.random() * L
        food_list.append(Food(x,y,z))
    return food_list

