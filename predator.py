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
        self.vx = v0
        self.vy = v0
        self.vz = v0
        self.catchRange = catchRange        # range in which the predator can catch a prey
        self.L = L                          # size of the box
        self.health = 100
        self.chasing = False     
        self.chasedBoid = None
        self.resting = False
       
    def getPosition(self):
        return (self.x,self.y,self.z)

    def getVelocity(self):
        return (self.vx,self.vy,self.vz)

    def getHealth(self):
        return self.health

    def getChasing(self):
        return self.chasing

    def getChasedBoid(self):
        return self.chasedBoid

    # function that updates the position of the predator
    def updatePosition(self):
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

    # function that updates the velocity of the predator
    def updateVelocity(self):
        if self.resting == True:
            self.vx = 0
            self.vy = 0
            self.vz = 0
        else:
            # if the predator is not chasing a prey, it will move randomly
            if self.chasing == False:
                self.vx = np.random.uniform(-1,1)
                self.vy = np.random.uniform(-1,1)
                self.vz = np.random.uniform(-1,1)

            else:  # if the predator is chasing a prey, it will move towards the prey
                # align velocity vector with prey position -> move towards prey
                self.vx = self.chasedBoid.x - self.x
                self.vy = self.chasedBoid.y - self.y
                self.vz = self.chasedBoid.z - self.z

            # normalize the velocity
            v_norm = np.linalg.norm([self.vx, self.vy, self.vz])
            print(v_norm)
            self.vx = self.vx*self.v0/v_norm
            self.vy = self.vy*self.v0/v_norm
            self.vz = self.vz*self.v0/v_norm

    # immobilize predator for a certain amount of time
    def rest(self):
        self.resting = True

    # function that checks whether the predator is resting
    def checkResting(self):
        return self.resting
    
    def awaken(self):
        self.resting = False

    # function that checks whether the target is in range of the predator
    def checkRangeAndChase(self, boid_target):
        # check if the target is in range of the predator
        if boid_target != None:
            self.chasing = True
            self.chasedBoid = boid_target

    # function that checks whether the predator is chasing a prey
    def getChasing(self):
        return self.chasing
    
    # function that checks whether the predator has caught a prey
    def checkCatch(self):
        if dist(self.getPosition(), self.chasedBoid.getPosition()) <= self.catchRange:
            return True
        else:
            return False

    # function that feeds the predator upon health every time step
    def feed(self):
        self.health += 10

    # check if the predator is ready to reproduce
    def checkReproduce(self):
        if self.health >= 150:
            # self.rest()
            return True
        else:
            return False

    # function that decays the predator's health every time step
    def healthDecay(self):
        self.health -= 1*self.dt

    # function that checks whether the predator is dead
    def checkDead(self):
        if self.health <= 0:
            return True
        else:
            return False

