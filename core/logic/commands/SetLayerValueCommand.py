from __future__ import annotations

from typing import Tuple

from core.constants import CellValue
from ..Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH

def __init__(self, i_coords: Tuple[int, int], i_value: CellValue):
    self.__coords = i_coords
    self.__value = i_value

def priority(self) -> int:
    """
    Computes a unique integer value for each cell and for the update case.
    """
    return WORLD_PRIORITY + self.__coords[0] + self.__coords[1] *WORLD_MAX_WIDTH