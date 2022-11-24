#class that defines the boid and their behaviour
import numpy as np
class Boid:
    def __init__(self,x:int,y:int,z:int,vx:int,vy:int,vz:int):
       self.x = x
       self.y = y
       self.z = z
       self.vx = vx
       self.vy = vy
       self.vz = vz
       self.smallflock = []
       self.largeflock = []
       self.predatorflock = []
       self.foodflock = []
    
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
        Ccohesion = 1
        Calignment = 1
        Cseparation = 1
        Cpredators = 1
        Cfood = 1
        dt = 0.01
        v0 = 1
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
        fx = np.mean([i.x for i in self.foodflock])-self.x
        fy = np.mean([i.y for i in self.foodflock])-self.y
        fz = np.mean([i.z for i in self.foodflock])-self.z

        #update
        self.vx += (Ccohesion*cx + Cseparation*sx + Calignment*lx + Cpredators*px + Cfood*fx)*dt
        self.vy += (Ccohesion*cy + Cseparation*sy + Calignment*ly + Cpredators*py + Cfood*fy)*dt
        self.vz += (Ccohesion*cz + Cseparation*sz + Calignment*lz + Cpredators*pz + Cfood*fz)*dt
        v = np.sqrt(self.vx**2+self.vy**2+self.vz**2)
        self.vx = self.vx*v0/v
        self.vy = self.vy*v0/v
        self.vz = self.vz*v0/v
        
    def updateSmallFlock(self,boids:list,neighbours:list):
        self.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(self)]]
        
    def updateLargeFlock(self,boids:list,neighbours:list):
        self.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(self)]]
        
    def updatePredators(self,predators:list,neighbours:list):
        self.smallflock = [predators[neighbour] for neighbour in neighbours[predators.index(self)]]
        
    def updateFoodFlock(self,food:list,neighbours:list):
        self.foodlist = [food[neighbour] for neighbour in neighbours[food.index(self)]]
        
        
        