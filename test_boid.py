from boid import Boid
from find_neighbours import findNeighbours

# Unit test for boid.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/


def test_updatePosition():
    testBoid = Boid(0,0,0,1,-1,0)
    testBoid.updatePosition()

    assert testBoid.x == 1, "x position not updated correctly"
    assert testBoid.y == -1, "y position not updated correctly"
    assert testBoid.z == -0, "z position not updated correctly"
    
def test_findNeighbours():
    r = 2
    L = 10
    testBoid1 = Boid(0,0,0,1,-1,0)
    testBoid2 = Boid(1,0,0,1,-1,0)
    testBoid3 = Boid(2,2,2,1,-1,0)
    
    boids = [testBoid1, testBoid2, testBoid3]
    
    neighbours = findNeighbours(boids, r, L)
    
    for boid in boids:
        boid.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(boid)]]
        
    print(testBoid1)
    print(testBoid2)
    print(testBoid3)
    print(testBoid1.smallflock)
    print(testBoid2.smallflock)
    
    assert testBoid1 in testBoid1.smallflock, "smallflock not updated correctly"
    assert testBoid2 in testBoid1.smallflock, "smallflock not updated correctly"
    assert testBoid3 not in testBoid1.smallflock, "smallflock not updated correctly"
    
    
    
    
    