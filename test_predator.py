from predator import Predator
from boid import Boid
import numpy as np
from find_neighbours import findClosestTarget

# Unit test for predator.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/

def test_getHealth():
    test_predator = Predator(0,0,0,1,2,100,1)
    assert test_predator.getHealth() == 100, "Health not initialized correctly"


def test_getPosition():
    test_predator = Predator(10,10,99.9,1,2,100,1)
    assert test_predator.getPosition() == (10,10,99.9), "Position not initialized correctly"


def test_feed():
    test_predator = Predator(0,0,0,1,2,100,1)
    test_predator.feed()

    assert test_predator.health == 150, "Health not updated correctly"

def test_CheckRangeAndChase():

    r_B = 10  # range of boid sensing
    L = 100  # length of the box

    ## test boid out of range ##
    test_boids = [Boid(10,10,10,1,1,1,1,1,1,1,L)] 
    test_predators = [Predator(0,0,0,1,2,100,1)]

    boid_targets = findClosestTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == None, "Boid should not be in range"
    test_predators[0].checkRangeAndChase(boid_targets[0])
    assert test_predators[0].chasing == False, "Predator should not be chasing"
    assert test_predators[0].chasedBoid == None, "Predator should not have a chased boid"

    ## test boids with one in range ##
    test_predators = [Predator(0,0,0,1,2,100,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1,L), Boid(5,5,5,1,1,1,1,1,1,1,L)]

    boid_targets = findClosestTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == test_boids[1], "Boid should be in range"
    test_predators[0].checkRangeAndChase(boid_targets[0]) == True
    assert test_predators[0].chasing == True, "Predator should be chasing"
    assert test_predators[0].chasedBoid == test_boids[1], "Predator should have a chased boid"

    ## test boids with two in range ##
    test_predators = [Predator(0,0,0,1,2,100,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1,L), Boid(5,5,5,1,1,1,1,1,1,1,L), Boid(2,2,2,1,1,1,1,1,1,1,L)]

    boid_targets = findClosestTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == test_boids[2], "Should chase closest boid in range"
    test_predators[0].checkRangeAndChase(boid_targets[0]) == False
    assert test_predators[0].chasing == True, "Predator should be chasing"
    assert test_predators[0].chasedBoid == test_boids[2], "Predator should have a chased boid"

    ## test with multiple predators ##
    test_predators = [Predator(0,0,0,1,2,100,1), Predator(20,20,20,1,2,100,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1,L), Boid(5,5,5,1,1,1,1,1,1,1,L), Boid(15,15,15,1,1,1,1,1,1,1,L)]

    boid_targets = findClosestTarget(test_predators, test_boids, r_B, L)

    for predator in test_predators:
        predator.checkRangeAndChase(boid_targets[test_predators.index(predator)]) == True

    assert test_predators[0].chasedBoid == test_boids[1], "Predator should have a chased boid"
    assert test_predators[1].chasedBoid == test_boids[2], "Predator should have a chased boid"   

def test_checkCatch():
    r_S = 2  # range of boid catching
    L = 100  # length of the box

    ## test boid out of range to catch ##
    test_predators = [Predator(0,0,0,1,2,100,1)]
    test_boids = [Boid(3,3,3,1,1,1,1,1,1,1,L)]

    boid_catches = findClosestTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == None, "Predator should not have a caught boid"

    ## test boid in range to catch ##
    test_predators = [Predator(0,0,0,1,2,100,1)]
    test_boids = [Boid(1,1,1,1,1,1,1,1,1,1,L)]

    boid_catches = findClosestTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == test_boids[0], "Predator should have a caught boid"

    ## test multiple boids in range to catch ##
    test_predators = [Predator(0,0,0,1,2,100,1)]
    test_boids = [Boid(1,1,1,1,1,1,1,1,1,1,L), Boid(2,1,1,1,1,1,1,1,1,1,L)]

    boid_catches = findClosestTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == test_boids[0], "Predator should have closest boid"

def test_updatePosition():
    test_predator = Predator(0,0,0,1,2,100,1)
    test_predator.updatePosition()

    assert test_predator.x == 1, "x position not updated correctly"
    assert test_predator.y == 1, "y position not updated correctly"
    assert test_predator.z == 1, "z position not updated correctly"

def test_updateVelocity():
    L = 100  # length of the box
    # test boid out of range
    test_boids = [Boid(50,50,50,1,1,1,1,1,1,1,L)] 
    # check for range, should be False

    test_predators = [Predator(0,0,0,1,2,100,1)]

    boid_targets = findClosestTarget(test_predators, test_boids, 10, 100)
    test_predators[0].checkRangeAndChase(boid_targets[0])
    test_predators[0].updateVelocity()
    print(test_predators[0].vx, test_predators[0].vy, test_predators[0].vz)

    assert test_predators[0].chasing == False, "Predator should not be chasing"
    assert np.abs(test_predators[0].vx) <= 1, "x velocity not updated correctly"
    assert np.abs(test_predators[0].vy) <= 1, "y velocity not updated correctly"
    assert np.abs(test_predators[0].vz) <= 1, "z velocity not updated correctly"

    # test boid in range, see that velocity is aligned with boid
    test_boids = [Boid(1,1,1,1,1,1,1,1,1,1,L)]
    test_predators = [Predator(0,0,0,1,2,100,1)]

    boid_targets = findClosestTarget(test_predators, test_boids, 10, 100)
    test_predators[0].checkRangeAndChase(boid_targets[0])

    test_predators[0].updateVelocity()

    assert test_predators[0].chasing is True, "Predator should be chasing"
    print(test_predators[0].getVelocity())
    print(np.linalg.norm(test_predators[0].getVelocity()))
    # check that velocity is aligned with boid
    assert test_predators[0].vx == 1/np.sqrt(3), "x velocity not updated correctly"
    assert test_predators[0].vy == 1/np.sqrt(3), "y velocity not updated correctly"
    assert test_predators[0].vz == 1/np.sqrt(3), "z velocity not updated correctly"

    
