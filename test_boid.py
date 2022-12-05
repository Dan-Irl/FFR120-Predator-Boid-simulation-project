from boid import Boid
from find_neighbours import findNeighbours, findTarget
from food import Food

# Unit test for boid.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/
    
def test_findNeighbours():
    r = 2
    L = 10
    testBoid1 = Boid(0,0,0,1,1,1,1,1,1,1,L)
    testBoid2 = Boid(0,1,0,1,1,1,1,1,1,1,L)
    testBoid3 = Boid(3,9,4,1,1,1,1,1,1,1,L)
    
    boids = [testBoid1, testBoid2, testBoid3]
    
    neighbours = findNeighbours(boids, r, L)
    
    for boid in boids:
        boid.smallflock = [boids[neighbour] for neighbour in neighbours[boids.index(boid)]]
    
    assert testBoid1 in testBoid1.smallflock, "smallflock not updated correctly"
    assert testBoid2 in testBoid1.smallflock, "smallflock not updated correctly"
    assert testBoid3 not in testBoid1.smallflock, "smallflock not updated correctly"
    
    
def test_updateSmallFlock():
    r = 5
    L = 10
    testBoid1 = Boid(0,0,0,1,1,1,1,1,1,1,L)
    testBoid2 = Boid(0,1,0,1,1,1,1,1,1,1,L)
    testBoid3 = Boid(0,0,0,1,1,1,1,1,1,1,L)
    
    boids = [testBoid1, testBoid2, testBoid3]
    
    neighbours = findNeighbours(boids, r, L)
    
    
    testBoid1.updateSmallFlock(boids, neighbours)
    
    assert testBoid1 in testBoid1.smallflock, "smallflock not updated correctly"
    assert testBoid2 in testBoid1.smallflock, "smallflock not updated correctly"
    
    
def test_updateLargeFlock():
    r = 5
    L = 10
    testBoid1 = Boid(0,0,0,1,1,1,1,1,1,1,L)
    testBoid2 = Boid(0,1,0,1,1,1,1,1,1,1,L)
    testBoid3 = Boid(0,3,2,1,1,1,1,1,1,1,L)
    
    boids = [testBoid1, testBoid2, testBoid3]
    
    neighbours = findNeighbours(boids, r, L)
    
    testBoid1.updateLargeFlock(boids, neighbours)
    
    assert testBoid1 in testBoid1.largeflock, "largeflock not updated correctly"
    assert testBoid2 in testBoid1.largeflock, "largeflock not updated correctly"
    assert testBoid3 in testBoid1.largeflock, "largeflock not updated correctly"
    
    
def test_findFood():
    r = 10
    L = 20
    testBoid1 = Boid(0,0,0,1,1,1,1,1,1,1,L)
    testBoid2 = Boid(10,10,10,1,1,1,1,1,1,1,L)
    testBoid3 = Boid(0,0,2,1,1,1,1,1,1,1,L)
    
    food1 = Food(1,1,1)
    food2 = Food(10,10,11)

    boids = [testBoid1, testBoid2, testBoid3]

    foods = [food1,food2]

    closestFood = findTarget(boids,foods,r,L)
    
    #Sets the closest food for each boid if it is within range
    for boid in boids:
        boid.foodlist = closestFood[boids.index(boid)]
    
    assert food1 == testBoid1.foodlist, "closest food not found"
    assert food2 == testBoid2.foodlist, "closest food not found"
    assert food1 == testBoid3.foodlist, "closest food not found"
