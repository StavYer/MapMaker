from __future__ import annotations
from typing import TYPE_CHECKING

from core.constants import CellValue, checkCellValue
from tools.tilecodes import mask4, code4
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
        
        if self._unit is not None:
            return False

        coords = self._coords
        world = i_logic.world
        # Check if the coordinates are within the world bounds
        if not world.contains(coords):
            return False
        
        objectsValue = world.objects.get_cell_value((coords[0], coords[1]))
        if value == CellValue.NONE:
            # If removing value, ensure it is already removed
            if objectsValue == CellValue.NONE:
                return False
        else:
            # If setting value, ensure it is not already set
            if objectsValue != CellValue.NONE:
                return False

            # Ensure the cell is not sea
            if world.ground.get_cell_value((coords[0], coords[1])) == CellValue.GROUND_SEA:
                return False

            impassableLayer = world.impassable
            impassableValue = impassableLayer.get_cell_value((coords[0], coords[1]))

            # If we have a river
            if impassableValue == CellValue.IMPASSABLE_RIVER:
                # Value must be a road type
                if value not in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:
                    return False
                
                neighbors = impassableLayer.getNeighbors4(coords)
                mask = mask4(neighbors, CellValue.IMPASSABLE_RIVER)
                code = code4(mask)
                # If not horizontal or vertical river
                if code not in [6,9]:
                    return False
            else:
                # In the general case, can't build if value already set
                if impassableValue != CellValue.NONE:
                    return False

        return True

    # Execute the command to set the object value
    def execute(self, i_logic: Logic):
        coords = self._coords
        value = self._value
        objects = i_logic.world.objects
        # Set the cell value in the objects layer
        objects.set_cell_value(coords[0], coords[1], value)
        objects.notifyCellChanged(coords)
    
        # If fill is enabled, recursively add commands for adjacent cells
        if hasattr(self, '_fill') and self._fill:
            x, y = coords[0], coords[1]
            i_logic.addCommand(SetObjectsValueCommand((x + 1, y), value, self._unit, True))
            i_logic.addCommand(SetObjectsValueCommand((x - 1, y), value, self._unit, True))
            i_logic.addCommand(SetObjectsValueCommand((x, y + 1), value, self._unit, True))
            i_logic.addCommand(SetObjectsValueCommand((x, y - 1), value, self._unit, True))
