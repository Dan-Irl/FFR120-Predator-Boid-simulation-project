from boid import boid

# Unit test for boid.py

# Check here how to write tests (install pytest first):
# https://docs.pytest.org/en/latest/


def test_updatePosition():
    testBoid = boid(0,0,0,1,-1,0,[],[],0)
    testBoid.updatePosition()

    assert testBoid.x == 1, "x position not updated correctly"
    assert testBoid.y == -1, "y position not updated correctly"
    assert testBoid.z == -0, "z position not updated correctly"
    