import numpy as np
from food import Food
from boid import Boid
from find_neighbours import findNeighbours, findTarget, findClosestTarget

# Unit test for food.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/


def test_findTarget():
    r_FC = 2
    L = 100

    testFoods = [Food(0,0,0), Food(5,5,5)]
    testBoids = [Boid(0,0,0,1,1,1,1,1,1,1,L)]

    food_boid_neighbours = findClosestTarget(testFoods, testBoids, r_FC, L)

    assert food_boid_neighbours[0] == testBoids[0], "boid not identified as in range"
    assert food_boid_neighbours[1] == None, "boid identified as in range when it is not"

    consumed_foods = [testFoods[i] for i in range(len(testFoods)) if food_boid_neighbours[i] is not None]
    for consumed_food in consumed_foods:
        assert consumed_food in testFoods, "food not consumed correctly"