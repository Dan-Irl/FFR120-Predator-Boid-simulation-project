#class that defines the predator and their behaviour
class Predator:
    def __init__(self,x,y,z):
       self.x = x
       self.y = y
       self.z = z
       self.vx = 0
       self.vy = 0
       self.vz = 0
       
    #function that updates the position of the predator
    def updatePosition(self):
        self.x += self.x + self.vx
        self.y += self.y + self.vy
        self.z += self.z + self.vz