# class that defines the predators and their behaviour

class Predator:
    def __init__(self,x,y,z):
       self.x = x
       self.y = y
       self.z = z
       self.vx = 0
       self.vy = 0
       self.vz = 0
       self.chasing = False     #indicates whether the predator is chasing a prey
       
    # function that updates the position of the predator
    def updatePosition(self):
        self.x += self.x + self.vx
        self.y += self.y + self.vy
        self.z += self.z + self.vz

    # function that updates the velocity of the predator
    def updateVelocity(self, boids, predators):
        # if the predator is not chasing a prey, it will move randomly
        if self.chasing == False:
            self.vx = random.uniform(-1,1)
            self.vy = random.uniform(-1,1)
            self.vz = random.uniform(-1,1)
        # if the predator is chasing a prey, it will move towards the prey
        else:
            # find the closest prey
            closest = boids[0]
            for boid in boids:
                if distance(self, boid) < distance(self, closest):
                    closest = boid
            # move towards the closest prey
            self.vx = closest.x - self.x
            self.vy = closest.y - self.y
            self.vz = closest.z - self.z
    
    # function that checks whether the predator is chasing a prey
    def checkChasing(self, boids):
        # if the predator is not chasing a prey, it will check if there is a prey in its sensing radius
        if self.chasing == False:
            for boid in boids:
                if distance(self, boid) < r_B:
                    self.chasing = True
                    break
        # if the predator is chasing a prey, it will check if the prey is still in its sensing radius
        else:
            for boid in boids:
                if distance(self, boid) > r_B:
                    self.chasing = False
                    break
    
    # function that checks whether the predator has caught a prey
    def checkCaught(self, boids):
        for boid in boids:
            if distance(self, boid) < r_S:
                boids.remove(boid)
    
