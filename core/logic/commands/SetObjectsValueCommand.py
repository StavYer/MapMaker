from __future__ import annotations
from typing import TYPE_CHECKING

from core.constants import CellValue, checkCellValue
from .SetLayerValueCommand import SetLayerValueCommand
if TYPE_CHECKING:
    from ..Logic import Logic

class SetObjectsValueCommand(SetLayerValueCommand):
    # Check if the command can be executed
    def check(self, i_logic: Logic) -> bool:
        value = self._value
        # Validate the cell value for objects
        if not checkCellValue("objects", value):
            return False

        coords = self._coords
        world = i_logic.world
        # Check if the coordinates are within the world bounds
        if not world.contains(coords):
            return False
        
        objectsValue = world.objects.get_cell_value(coords[0], coords[1])
        if value == CellValue.NONE:
            # If removing value, ensure it is already removed
            if objectsValue == CellValue.NONE:
                return False
        else:
            # If setting value, ensure it is not already set
            if objectsValue != CellValue.NONE:
                return False
            # Ensure the cell is not sea or impassable terrain
            if world.ground.get_cell_value(coords[0], coords[1]) == CellValue.GROUND_SEA:
                return False
            if world.impassable.get_cell_value(coords[0], coords[1]) != CellValue.NONE:
                return False

        return True

    # Execute the command to set the object value
    def execute(self, i_logic: Logic):
        coords = self._coords
        value = self._value
        world = i_logic.world
        # Set the cell value in the objects layer
        world.objects.set_cell_value(coords[0], coords[1], value)
