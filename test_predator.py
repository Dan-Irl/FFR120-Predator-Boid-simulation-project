from predator import Predator
from boid import Boid
import numpy as np
from find_neighbours import findTarget

# Unit test for predator.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/

def test_getHealth():
    test_predator = Predator(0,0,0,1,10,1)
    assert test_predator.getHealth() == 100, "Health not initialized correctly"


def test_getPosition():
    test_predator = Predator(-10,10,100,1,10,1)
    assert test_predator.getPosition() == (-10,10,100), "Position not initialized correctly"


def test_feed():
    test_predator = Predator(0,0,0,1,10,1)
    test_predator.feed()

    assert test_predator.health == 110, "Health not updated correctly"

def test_getChasing():
    test_predator = Predator(0,0,0,1,10,1)
    assert test_predator.getChasing() == False, "Chasing not initialized correctly"

def test_CheckRangeAndChase():

    r_B = 10  # range of boid sensing
    L = 100  # length of the box

    ## test boid out of range ##
    test_boids = [Boid(10,10,10,1,1,1,1,1,1,1)] 
    test_predators = [Predator(0,0,0,1,10,1)]

    boid_targets = findTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == None, "Boid should not be in range"
    assert test_predators[0].chasing == False, "Predator should not be chasing"
    assert test_predators[0].chasedBoid == None, "Predator should not have a chased boid"
    assert test_predators[0].checkRangeAndChase(boid_targets[0]) == False, "Predator should not be chasing"

    ## test boids with one in range ##
    test_predators = [Predator(0,0,0,1,10,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1), Boid(5,5,5,1,1,1,1,1,1,1)]

    boid_targets = findTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == test_boids[1], "Boid should be in range"
    assert test_predators[0].checkRangeAndChase(boid_targets[0]) == True, "Predator should be chasing"
    assert test_predators[0].chasing == True, "Predator should be chasing"
    assert test_predators[0].chasedBoid == test_boids[1], "Predator should have a chased boid"

    ## test boids with two in range ##
    test_predators = [Predator(0,0,0,1,10,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1), Boid(5,5,5,1,1,1,1,1,1,1), Boid(2,2,2,1,1,1,1,1,1,1)]

    boid_targets = findTarget(test_predators, test_boids, r_B, L)

    assert boid_targets[0] == test_boids[2], "Should chase closest boid in range"
    assert test_predators[0].chasing == True, "Predator should be chasing"
    assert test_predators[0].chasedBoid == test_boids[2], "Predator should have a chased boid"
    assert test_predators[0].checkRangeAndChase(boid_targets[0]) == True, "Predator should be chasing"

    ## test with multiple predators ##
    test_predators = [Predator(0,0,0,1,10,1), Predator(20,20,20,1,10,1)]
    test_boids = [Boid(49,49,49,1,1,1,1,1,1,1), Boid(5,5,5,1,1,1,1,1,1,1), Boid(15,15,15,1,1,1,1,1,1,1)]

    boid_targets = findTarget(test_predators, test_boids, r_B, L)

    for predator in test_predators:
        assert predator.checkRangeAndChase(boid_targets[test_predators.index(predator)]) == True, "Predator should be chasing"

    assert test_predators[0].chased_boid == test_boids[1], "Predator should have a chased boid"
    assert test_predators[1].chased_boid == test_boids[2], "Predator should have a chased boid"   
    assert test_predator.chased_boid == test_boids[0], "Predator should have a chased boid"

def test_checkCatch():
    r_S = 2  # range of boid catching
    L = 100  # length of the box

    ## test boid out of range to catch ##
    test_predators = [Predator(0,0,0,1,10,1)]
    test_boids = [Boid(3,3,3,1,1,1,1,1,1,1)]

    boid_catches = findTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == None, "Predator should not have a caught boid"

    ## test boid in range to catch ##
    test_predators = [Predator(0,0,0,1,10,1)]
    test_boids = [Boid(1,1,1,1,1,1,1,1,1,1)]

    boid_catches = findTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == test_boids[0], "Predator should have a caught boid"

    ## test multiple boids in range to catch ##
    test_predators = [Predator(0,0,0,1,10,1)]
    test_boids = [Boid(1,1,1,1,1,1,1,1,1,1), Boid(2,1,1,1,1,1,1,1,1,1)]

    boid_catches = findTarget(test_predators, test_boids, r_S, L)

    assert boid_catches[0] == test_boids[0], "Predator should have closest boid"

def test_updatePosition():
    test_predator = Predator(0,0,0,1,10,1)
    test_predator.updatePosition()

    assert test_predator.x == 1, "x position not updated correctly"
    assert test_predator.y == 1, "y position not updated correctly"
    assert test_predator.z == 1, "z position not updated correctly"

def test_updateVelocity():
    # test boid out of range
    test_boids = [Boid(100,100,100,1,1,1,1,1,1,1)] 
    # check for range, should be False


    test_predator = Predator(0,0,0,1,10,1)
    test_predator.updateVelocity()

    assert np.abs(test_predator.vx) <= 1, "x velocity not updated correctly"
    assert np.abs(test_predator.vy) <= 1, "y velocity not updated correctly"
    assert np.abs(test_predator.vz) <= 1, "z velocity not updated correctly"

    # test boid in range, see that velocity is aligned with boid
