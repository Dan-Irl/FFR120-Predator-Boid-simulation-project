# class that defines the predators and their behaviour
import numpy as np
from math import dist

class Predator:
    def __init__(self,x:float,y:float,z:float,v0:float,catchRange,L:float,dt:float):
        self.x = x
        self.y = y
        self.z = z
        self.v0 = v0
        self.dt = dt
        self.vx = np.random.uniform(-1,1)*v0
        self.vy = np.random.uniform(-1,1)*v0
        self.vz = np.random.uniform(-1,1)*v0
        self.catchRange = catchRange        # range in which the predator can catch a prey
        self.L = L                          # size of the box
        self.health = 100
        self.chasing = False     
        self.chasedBoids = []
        self.resting = False
       
    def getPosition(self) -> tuple:
        """Returns the position of the predator"""
        return (self.x,self.y,self.z)

    def getVelocity(self) -> tuple:
        """Returns velocity of predator"""
        return (self.vx,self.vy,self.vz)

    def getchasedBoids(self):
        """Returns the chased boid of the predator"""
        return self.chasedBoids
    
    def updatePosition(self):
        """Updates the position of the predator using perodic boundary condictions."""
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

    def updateVelocity(self):
        """function that updates the velocity of the predator"""
        if self.resting == True:
            self.vx = 0.25*np.random.normal(self.vy,abs(self.vz*0.5))
            self.vy = 0.25*np.random.normal(self.vy,abs(self.vz*0.5))
            self.vz = 0.25*np.random.normal(self.vy,abs(self.vz*0.5))
        else:
            # if the predator is not chasing a prey, it will move randomly
            if self.chasing == False:
                
                self.vx = np.random.normal(self.vx,abs(self.vx*0.5))
                self.vy = np.random.normal(self.vy,abs(self.vy*0.5))
                self.vz = np.random.normal(self.vz,abs(self.vz*0.5))

            else:  # if the predator is chasing a prey, it will move towards the prey
                # align velocity vector with prey position -> move towards prey
                self.vx = np.mean([b.x for b in self.chasedBoids]) - self.x
                self.vy = np.mean([b.y for b in self.chasedBoids]) - self.y
                self.vz = np.mean([b.z for b in self.chasedBoids]) - self.z

            # normalize the velocity
            v_norm = np.linalg.norm([self.vx, self.vy, self.vz])
            self.vx = self.vx*self.v0/v_norm
            self.vy = self.vy*self.v0/v_norm
            self.vz = self.vz*self.v0/v_norm

    def rest(self):
        """Sets the predator state to resting"""
        self.resting = True

    def checkResting(self):
        """Returns True if perdator is resting otherwise False"""
        return self.resting
    
    def awaken(self):
        """Sets the predator state to not resting"""
        self.resting = False

    def checkRangeAndChase(self, boid_targets):
        """Checks if predator is in range of target and if so, starts chasing it"""
        if len(boid_targets) > 0:
            self.chasing = True
            self.chasedBoids = boid_targets
    
    def checkIfCaught(self) -> bool:
        """Checks if predator has caught prey and if so, returns True"""
        boid_in_range_bools = [dist(self.getPosition(), b.getPosition()) <= self.catchRange for b in self.chasedBoids]
        indices_in_range = [i for i, x in enumerate(boid_in_range_bools) if x]
        if len(indices_in_range) == 0:
            return None
        return self.chasedBoids[np.random.choice(indices_in_range)]
        
    def feed(self, healthGain) -> None:
        """Increases health of predator upon feeding"""
        self.health += healthGain

    def checkReproduce(self, reproduction_cutoff) -> bool:
        """Checks if predator is ready to reproduce and if so, returns True otherwise False"""
        return self.health >= reproduction_cutoff

    def healthDecay(self):
        """Decays health of predator every time step"""
        self.health -= self.dt

