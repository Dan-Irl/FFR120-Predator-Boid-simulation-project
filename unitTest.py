from boid import boid

boids = [boid() for boid in range(10)]

for boid in boids:
boid.x = 1
boid.vx = 1

boid.updateVelocity()

if boid.x = 2:
    bool = True
    
    
else:
    bool = False
    
print(f'updateVelocity() : {bool}')