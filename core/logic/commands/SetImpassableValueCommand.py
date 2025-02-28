
from __future__ import annotations

from core.constants import CellValue, checkCellValue
from typing import TYPE_CHECKING

from core.constants import CellValue, checkCellValue
from .SetLayerValueCommand import SetLayerValueCommand
if TYPE_CHECKING:
    from ..Logic import Logic

class SetImpassableValueCommand(SetLayerValueCommand):
    # Check if the command can be executed
    def check(self, i_logic: Logic) -> bool:
        value = self._value
        # Verify if the value to set is a valid impassable cell value
        if not checkCellValue("impassable", value):
            return False

        coords = self._coords
        world = i_logic.world
        # Check if the coordinates are within the world bounds
        if not world.contains(coords):
            return False

        impassableValue = world.impassable.get_cell_value(coords[0], coords[1])
        if value == CellValue.NONE:
            # If the value to set is NONE, ensure it is not already NONE
            if impassableValue == CellValue.NONE:  # Value already removed
                return False
        else:
            # If the value to set is not NONE, ensure it is not already set
            if impassableValue != CellValue.NONE:  # Value already set
                return False
            # Ensure the ground cell is not SEA
            if world.ground.get_cell_value(coords[0], coords[1]) == CellValue.GROUND_SEA:
                return False
            # Ensure there are no objects in the cell
            if world.objects.get_cell_value(coords[0], coords[1]) != CellValue.NONE:
                return False

        return True
        
    # Execute the command to set the impassable value
    def execute(self, i_logic: Logic):
        coords = self._coords
        value = self._value
        world = i_logic.world
        # Set the impassable cell value in the world
        world.impassable.set_cell_value(coords[0], coords[1], value)
        
        # If fill is enabled, recursively add commands for adjacent cells
        if hasattr(self, '_fill') and self._fill:
            x, y = coords[0], coords[1]
            i_logic.addCommand(SetImpassableValueCommand((x + 1, y), value, True))
            i_logic.addCommand(SetImpassableValueCommand((x - 1, y), value, True))
            i_logic.addCommand(SetImpassableValueCommand((x, y + 1), value, True))
            i_logic.addCommand(SetImpassableValueCommand((x, y - 1), value, True))
