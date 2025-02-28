from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from core.constants import CellValue
from ..Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH


class SetLayerValueCommand(Command):
    def __init__(self, i_coords: Tuple[int, int], i_value: CellValue):
        self._coords = i_coords
        self._value = i_value

    def priority(self) -> int:
        """
        Computes a unique integer value for each cell and for the update case.
        """
        return WORLD_PRIORITY + self._coords[0] + self._coords[1] *WORLD_MAX_WIDTH