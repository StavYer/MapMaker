import pytest

from state import World
from state.constants import LAYER_GROUND_SEA, LAYER_GROUND_EARTH


def test_setget():
    # Initialize the world with dimensions 14x7
    world = World(14, 7)

    # Verify that the world dimensions are set correctly
    assert world.width == 14
    assert world.height == 7

    # Verify that all tiles are initialized to LAYER_GROUND_SEA (0)
    for y in range(world.height):
        for x in range(world.width):
            assert world.get_cell_value(x, y) == LAYER_GROUND_SEA

    # Set a specific tile (3, 4) to LAYER_GROUND_EARTH (1)
    world.set_cell_value(3, 4, LAYER_GROUND_EARTH)

    # Verify that only the tile (3, 4) has changed, and others remain unchanged
    for y in range(world.height):
        for x in range(world.width):
            if x == 3 and y == 4:
                assert world.get_cell_value(x, y) == LAYER_GROUND_EARTH
            else:
                assert world.get_cell_value(x, y) == LAYER_GROUND_SEA
