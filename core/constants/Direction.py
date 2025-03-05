from enum import Enum


class Direction(Enum):
    """Directions for connected tiles and navigation"""
    LEFT = 0
    TOP = 1
    BOTTOM = 2
    RIGHT = 3


# Tuple of all directions for iteration
directions = (Direction.LEFT, Direction.TOP, Direction.BOTTOM, Direction.RIGHT)