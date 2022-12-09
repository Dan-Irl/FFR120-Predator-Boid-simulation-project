# class that defines the boid and their behaviour

import numpy as np
class Boid:
    def __init__(self,x:float,y:float,z:float,v0:float,c_cohesion:float,c_alignment:float,c_separation:float,c_predators:float,c_food:float,dt:float,L:float):
            
        self.x = x
        self.y = y
        self.z = z
        self.vx = np.random.uniform(-1,1)*v0
        self.vy = np.random.uniform(-1,1)*v0
        self.vz = np.random.uniform(-1,1)*v0
        self.v0 = v0
        self.c_cohesion = c_cohesion
        self.c_separation = c_separation
        self.c_alignment = c_alignment
        self.c_predators = c_predators
        self.c_food = c_food
        self.dt = dt
        self.L = L
        self.smallflock = []
        self.largeflock = []
        self.predatorFlock = []
        # self.foodList = []
        self.closestFood = None

    # enables checking equality of boids, among other things
    def __eq__(self, other):
        if isinstance(other, Boid):
            return self.x == other.x and self.y == other.y and self.z == other.z
    
    #function that returns the position of the boid
    def getPosition(self):
        return (self.x,self.y,self.z)

    def getVelocity(self):
        return (self.vx,self.vy,self.vz)
       
    #function that updates the position of the boid
    def updatePosition(self):
        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.z += self.vz*self.dt

        # check (periodic) boundary conditions
        if self.x < 0:
            self.x += self.L
        elif self.x > self.L:
            self.x -= self.L
        if self.y < 0:
            self.y += self.L
        elif self.y > self.L:
            self.y -= self.L
        if self.z < 0:
            self.z += self.L
        elif self.z > self.L:
            self.z -= self.L
    
    #function that updates the position of the boid using cohesion, separation,
    #alignment, predators, food
    def updateVelocity(self):
        if len(self.largeflock)>0:
            #cohesion
            cx = np.mean([i.x for i in self.largeflock])-self.x
            cy = np.mean([i.y for i in self.largeflock])-self.y
            cz = np.mean([i.z for i in self.largeflock])-self.z
            #alignment
            lx = 1/len(self.largeflock)*sum([i.vx for i in self.largeflock])
            ly = 1/len(self.largeflock)*sum([i.vy for i in self.largeflock])
            lz = 1/len(self.largeflock)*sum([i.vz for i in self.largeflock])
        else:
            cx = 0
            cy = 0
            cz = 0
            lx = 0
            ly = 0
            lz = 0
        
        if len(self.smallflock)>0:
            #separation
            sx = sum([self.x-i.x for i in self.smallflock])
            sy = sum([self.y-i.y for i in self.smallflock])
            sz = sum([self.z-i.z for i in self.smallflock])  
        else:
            sx = 0
            sy = 0
            sz = 0
        
        if len(self.predatorFlock)>0:
            #predator
            px = sum([self.x-i.x for i in self.predatorFlock])
            py = sum([self.y-i.y for i in self.predatorFlock])
            pz = sum([self.z-i.z for i in self.predatorFlock])
        else:
            px = 0
            py = 0
            pz = 0
        
        # if self.foodList is not None:
        if self.closestFood is not None:
            #food
            fx = self.closestFood.x - self.x
            fy = self.closestFood.y - self.y
            fz = self.closestFood.z - self.z
        else:
            fx = 0
            fy = 0
            fz = 0

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
        self.largeflock = [boids[neighbour] for neighbour in neighbours[boids.index(self)]]
        
    def updatePredators(self,predatorsInRange):
        self.predatorFlock = predatorsInRange
        
    # def updateFoodList(self, foodsInRange):         # Alternative 1: All foods in range
    #     if len(foodsInRange) > 0:      # all foods in range
    #         self.foodList = foodsInRange
    #     else:                                               
    #         self.foodList = []