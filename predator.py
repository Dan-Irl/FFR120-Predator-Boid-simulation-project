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
        self.vx = np.random.rand()*v0
        self.vy = np.random.rand()*v0
        self.vz = np.random.rand()*v0
        self.catchRange = catchRange        # range in which the predator can catch a prey
        self.L = L                          # size of the box
        self.health = 100
        self.chasing = False     
        self.chasedBoid = None
        self.resting = False
       
    def getPosition(self) -> tuple:
        """Returns the position of the predator"""
        return (self.x,self.y,self.z)

    def getVelocity(self) -> tuple:
        """Returns velocity of predator"""
        return (self.vx,self.vy,self.vz)

    def getChasedBoid(self):
        """Returns the chased boid of the predator"""
        return self.chasedBoid
    
    def updatePosition(self):
        """Updates the position of the predator using perodic boundary condictions."""
        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.z += self.vz*self.dt

        # check (periodic) boundary conditions
        if self.x < 0:
            self.x += self.L
            self.vx = -self.vx
        elif self.x > self.L:
            self.x -= self.L
            self.vx = -self.vx
        if self.y < 0:
            self.y += self.L
            self.vy = -self.vy
        elif self.y > self.L:
            self.y -= self.L
            self.vy = -self.vy
        if self.z < 0:
            self.z += self.L
            self.vz = -self.vz
        elif self.z > self.L:
            self.z -= self.L
            self.vz = -self.vz

    def updateVelocity(self):
        """function that updates the velocity of the predator"""
        if self.resting == True:
            self.vx = 0
            self.vy = 0
            self.vz = 0
        else:
            # if the predator is not chasing a prey, it will move randomly
            if self.chasing == False:
                
                self.vx = np.random.normal(self.vx,abs(self.vx*0.5))
                self.vy = np.random.normal(self.vy,abs(self.vy*0.5))
                self.vz = np.random.normal(self.vy,abs(self.vy*0.5))

            else:  # if the predator is chasing a prey, it will move towards the prey
                # align velocity vector with prey position -> move towards prey
                self.vx = np.mean([b.x for b in self.chasedBoid]) - self.x
                self.vy = np.mean([b.y for b in self.chasedBoid]) - self.y
                self.vz = np.mean([b.z for b in self.chasedBoid]) - self.z

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

    def checkRangeAndChase(self, boid_target):
        """Checks if predator is in range of target and if so, starts chasing it"""
        if boid_target is not None:
            self.chasing = True
            self.chasedBoid = boid_target
    
    def checkIfCaught(self):
        """Checks if predator has caught prey and if so, returns True"""
        return dist(self.getPosition(), self.chasedBoid.getPosition()) <= self.catchRange

    def feed(self, healthGain) -> None:
        """Increases health of predator upon feeding"""
        self.health += healthGain

    def checkReproduce(self, reproduction_cutoff) -> bool:
        """Checks if predator is ready to reproduce and if so, returns True otherwise False"""
        return self.health >= reproduction_cutoff

    def healthDecay(self):
        """Decays health of predator every time step"""
        self.health -= 5*self.dt

