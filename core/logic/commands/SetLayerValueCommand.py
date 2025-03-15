from __future__ import annotations

from typing import Tuple, Optional

from core.constants import CellValue
from ..Command import Command, WORLD_PRIORITY, WORLD_MAX_WIDTH
from ...state import Unit


class SetLayerValueCommand(Command):
    def __init__(self, i_coords: Tuple[int, int], i_value: CellValue,i_unit: Optional[Unit] = None, i_fill: bool = False):
        self._coords = i_coords
        self._value = i_value
        self._unit = i_unit
        self._fill = i_fill

    def priority(self) -> int:
        """
        Computes a unique integer value for each cell and for the update case.
        """
        return WORLD_PRIORITY + self._coords[0] + self._coords[1] *WORLD_MAX_WIDTH