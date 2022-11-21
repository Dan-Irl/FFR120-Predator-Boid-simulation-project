#class that defines the boid and their behaviour
class boid:
    def __init__(self,x:int,y:int,z:int,vx:int,vy:int,vz:int,smallflock:list,largeflock:list,predators:list):
       self.x = x
       self.y = y
       self.z = z
       self.vx = vx
       self.vy = vy
       self.vz = vz
       self.smallflock = smallflock
       self.largeflock = largeflock
       
    #function that updates the position of the boid
    def updatePosition(self):
        self.x += self.x + self.vx
        self.y += self.y + self.vy
        self.z += self.z + self.vz
    
    def updateVelocity(self):
        #cohesion
        xcom = np.mean([i.x for i in largeflock])
        ycom = np.mean([i.y for i in largeflock])
        zcom = np.mean([i.z for i in largeflock])
        
        cx = xcom-self.x
        cy = ycom-self.y
        cz = zcom-self.z
        
        #separation
        #alignment
        
        self.vx += Ccohesion*cx
        self.vy += Ccohesion*cy
        self.vz += Ccohesion*cz
        
        
        