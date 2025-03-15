from __future__ import annotations
from typing import TYPE_CHECKING

from core.constants import CellValue
from core.state import Unit
from .SetLayerValueCommand import SetLayerValueCommand

if TYPE_CHECKING:
    from ..Logic import Logic


class SetUnitsCellCommand(SetLayerValueCommand):
    """Command to set or remove a unit on a cell"""

    def check(self, logic: Logic) -> bool:
        """Check if the command can be executed"""
        if self._value not in [CellValue.NONE, CellValue.UNITS_UNIT]:
            return False

        cell = self._coords
        world = logic.world
        if not world.contains(cell):
            return False

        unitsValue = world.units.get_cell_value(cell)
        if self._value == CellValue.NONE or self._unit is None:
            if unitsValue == CellValue.NONE:  # Unit already removed
                return False
        else:
            if not isinstance(self._unit, Unit):
                return False
            if unitsValue != CellValue.NONE:  # Unit already in there
                return False
            if world.ground.get_cell_value(cell) == CellValue.GROUND_SEA:  # Can't put a unit on the sea
                return False
            
            # Impassable
            impassableValue = world.impassable.get_cell_value(cell)
            if impassableValue == CellValue.IMPASSABLE_RIVER:  # River case
                objectsValue = world.objects.get_cell_value(cell)
                if objectsValue not in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:  # Can walk on bridge
                    return False
            else:  # General case
                if impassableValue != CellValue.NONE:  # Can't walk on mountains etc.
                    return False

        return True

    def execute(self, logic: Logic, simulate: bool = False):
        """Execute the command"""
        cell = self._coords
        world = logic.world
        world.units.setUnit(cell, self._value, self._unit)
        world.units.notifyCellChanged(cell)

        if self._fill:
            x, y = cell[0], cell[1]
            logic.addCommand(SetUnitsCellCommand((x + 1, y), self._value, self._unit, True))
            logic.addCommand(SetUnitsCellCommand((x - 1, y), self._value, self._unit, True))
            logic.addCommand(SetUnitsCellCommand((x, y + 1), self._value, self._unit, True))
            logic.addCommand(SetUnitsCellCommand((x, y - 1), self._value, self._unit, True))
