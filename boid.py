#class that defines the boid and their behaviour

import numpy as np
class Boid:
    def __init__(self,x:float,y:float,z:float,v0:float,c_cohesion:float,c_alignment:float,c_separation:float,c_predators:float,c_food:float,dt:float):
        
        
        self.x = x
        self.y = y
        self.z = z
        self.vx = v0
        self.vy = v0
        self.vz = v0
        self.v0 = v0
        self.c_cohesion = c_cohesion
        self.c_separation = c_separation
        self.c_alignment = c_alignment
        self.c_predators = c_predators
        self.c_food = c_food
        self.smallflock = []
        self.largeflock = []
        self.predatorflock = []
        self.foodlist = []
    
    #function that returns the position of the boid
    def getPosition(self):
        return (self.x,self.y,self.z)
       
    #function that updates the position of the boid
    def updatePosition(self):
        self.x += self.x + self.vx
        self.y += self.y + self.vy
        self.z += self.z + self.vz
    
    #function that updates the position of the boid using cohesion, separation,
    #alignment, predators, food
    def updateVelocity(self):
        #cohesion
        cx = np.mean([i.x for i in self.largeflock])-self.x
        cy = np.mean([i.y for i in self.largeflock])-self.y
        cz = np.mean([i.z for i in self.largeflock])-self.z
        
        #separation
        sx = sum([self.x-i.x for i in self.smallflock])
        sy = sum([self.y-i.y for i in self.smallflock])
        sz = sum([self.z-i.z for i in self.smallflock])

        #alignment
        lx = 1/len(self.largeflock)*sum([i.vx for i in self.largeflock])
        ly = 1/len(self.largeflock)*sum([i.vy for i in self.largeflock])
        lz = 1/len(self.largeflock)*sum([i.vz for i in self.largeflock])
        
        #predator
        px = sum([self.x-i.x for i in self.predatorflock])
        py = sum([self.y-i.y for i in self.predatorflock])
        pz = sum([self.z-i.z for i in self.predatorflock])

        #food
        fx = np.mean([i.x for i in self.foodlist])-self.x
        fy = np.mean([i.y for i in self.foodlist])-self.y
        fz = np.mean([i.z for i in self.foodlist])-self.z

        #update
        self.vx += (self.c_cohesion*cx + self.c_separation*sx + self.c_alignment*lx + self.c_predators*px + self.c_food*fx)*self.dt
        self.vy += (self.c_cohesion*cy + self.c_separation*sy + self.c_alignment*ly + self.c_predators*py + self.c_food*fy)*self.dt
        self.vz += (self.c_cohesion*cz + self.c_separation*sz + self.c_alignment*lz + self.c_predators*pz + self.c_food*fz)*self.dt
        v = np.sqrt(self.vx**2+self.vy**2+self.vz**2)
        self.vx = self.vx*self.v0/v
        self.vy = self.vy*self.v0/v
        self.vz = self.vz*self.v0/v
        
    def updateSmallFlock(self,boids:list,neighbours:list):
        self.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(self)]]
        
    def updateLargeFlock(self,boids:list,neighbours:list):
        self.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(self)]]
        
    def updatePredators(self,predators:list,neighbours:list):
        self.smallflock = [predators[neighbour] for neighbour in neighbours[predators.index(self)]]
        
    def updateFoodFlock(self,food:list,neighbours:list):
        self.foodlist = [food[neighbour] for neighbour in neighbours[food.index(self)]]
        
        
        