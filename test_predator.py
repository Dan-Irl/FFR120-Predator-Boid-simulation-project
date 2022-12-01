from predator import Predator
from boid import Boid
import numpy as np

# Unit test for predator.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/

def test_get_health():
    test_predator = Predator(0,0,0,1,1)
    assert test_predator.get_health() == 100, "Health not initialized correctly"


def test_get_position():
    test_predator = Predator(-10,10,100,1,1)
    assert test_predator.get_position() == (-10,10,100), "Position not initialized correctly"


def test_feed():
    test_predator = Predator(0,0,0,1,1)
    test_predator.feed()

    assert test_predator.health == 110, "Health not updated correctly"

def test_get_chasing():
    test_predator = Predator(0,0,0,1,1)
    assert test_predator.get_chasing() == False, "Chasing not initialized correctly"

def test_check_chasing():
    ## test boid out of range ##
    test_boids = [Boid(100,100,100,1,1,1,1,1,1,1)] 
    # check for range, should be False


    test_predator = Predator(0,0,0,1,1)
    test_predator.check_chasing(test_boids)

    assert test_predator.chasing == False, "Predator should not be chasing"
    assert test_predator.chased_boid == None, "Predator should not have a chased boid"

    ## test boid in range ##
    test_boids = [Boid(0,0,0,1,1,1,1,1,1,1)] 
    # check for range, should be True


    test_predator = Predator(0,0,0,1,1)
    test_predator.check_chasing(test_boids)

    assert test_predator.chasing == True, "Predator should be chasing"
    assert test_predator.chased_boid == test_boids[0], "Predator should have a chased boid"

def test_get_chased_boid():
    test_predator = Predator(0,0,0,1,1)
    assert test_predator.get_chased_boid() == None, "Chased boid not initialized correctly"

def test_update_position():
    test_predator = Predator(0,0,0,1,1)
    test_predator.update_position()

    assert test_predator.x == 1, "x position not updated correctly"
    assert test_predator.y == 1, "y position not updated correctly"
    assert test_predator.z == 1, "z position not updated correctly"

def test_update_velocity():
    # test boid out of range
    test_boids = [Boid(100,100,100,1,1,1,1,1,1,1)] 
    # check for range, should be False


    test_predator = Predator(0,0,0,1,1)
    test_predator.update_velocity()

    assert np.abs(test_predator.vx) <= 1, "x velocity not updated correctly"
    assert np.abs(test_predator.vy) <= 1, "y velocity not updated correctly"
    assert np.abs(test_predator.vz) <= 1, "z velocity not updated correctly"

    # test boid in range, see that velocity is aligned with boid
