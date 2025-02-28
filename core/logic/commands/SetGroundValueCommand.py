from __future__ import annotations

from core.constants import CellValue, checkCellValue
from typing import TYPE_CHECKING

from core.constants import CellValue, checkCellValue
from .SetLayerValueCommand import SetLayerValueCommand
if TYPE_CHECKING:
    from ..Logic import Logic


class SetGroundValueCommand(SetLayerValueCommand):

    def check(self, i_logic: Logic) -> bool:
        # Check if the value is valid
        value = self._value
        if not checkCellValue("ground", value):
            return False

        coords = self._coords
        world = i_logic.world
        
        # Check if the coordinates are within the world bounds
        if not world.contains(coords):
            return False

        groundValue = world.ground.get_cell_value(coords[0], coords[1])
        
        # Check if the ground value is already set to the desired value
        if value == groundValue:
            return False
        
        # Additional checks if setting the value to sea, since we don't want to set
        # a sea with an object or impassable value
        if value == CellValue.GROUND_SEA:
            impassableValue = world.impassable.get_cell_value(coords[0], coords[1])
            if impassableValue != CellValue.NONE:
                return False

            objectsValue = world.objects.get_cell_value(coords[0], coords[1])
            if objectsValue != CellValue.NONE:
                return False

        return True

    def execute(self, i_logic: Logic):
        coords = self._coords
        value = self._value
        ground = i_logic.world.ground
        
        # Set the ground value at the specified coordinates
        ground.set_cell_value(coords[0], coords[1], value)

        # If fill is enabled, recursively add commands for adjacent cells
        if hasattr(self, '_fill') and self._fill:
            x, y = coords[0], coords[1]
            i_logic.addCommand(SetGroundValueCommand((x + 1, y), value, True))
            i_logic.addCommand(SetGroundValueCommand((x - 1, y), value, True))
            i_logic.addCommand(SetGroundValueCommand((x, y + 1), value, True))
            i_logic.addCommand(SetGroundValueCommand((x, y - 1), value, True))