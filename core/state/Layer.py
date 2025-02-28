# core/state/Layer.py
from typing import Tuple

from ..Listenable import Listenable
from .ILayerListener import ILayerListener
from ..constants.CellValue import CellValue


class Layer(Listenable[ILayerListener]):
    """A layer in the game world that can be observed for changes."""
    
    def __init__(self, input_width: int, input_height: int, input_defaultValue: CellValue):
        super().__init__()
        # size of our Layer. Should be immutable.
        self.__width = input_width
        self.__height = input_height
        # Value of every cell of the Layer. Should be immutable.
        # A 2d matrix - each row has width columns (initialized to default value)
        # and we have height rows
        self.__cells = []
        for y in range(input_height):
            row = [input_defaultValue] * input_width
            self.__cells.append(row)
    
    # Getter properties
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    # Getter and Setter for a single cell's value
    def get_cell_value(self, input_x: int, input_y: int) -> CellValue:
        # Assert that the coordinates are at between proper limits, otherwise notify
        assert 0 <= input_x < self.__width, f"invalid cell x coordinate: {input_x}"
        assert 0 <= input_y < self.__height, f"invalid cell y coordinate: {input_y}"

        return self.__cells[input_y][input_x]

    def set_cell_value(self, input_x: int, input_y: int, value: CellValue) -> None:
        # Same here
        assert 0 <= input_x < self.__width, f"invalid cell x coordinate: {input_x}"
        assert 0 <= input_y < self.__height, f"invalid cell y coordinate: {input_y}"
        self.__cells[input_y][input_x] = value
    
    # Layer listener notification method
    def notifyCellChanged(self, cell: Tuple[int, int]):
        """Notify all listeners that a cell has changed."""
        for listener in self.listeners:
            listener.cellChanged(self, cell)