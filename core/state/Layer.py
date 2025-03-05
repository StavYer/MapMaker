# core/state/Layer.py
from typing import Tuple, Optional

from ..Listenable import Listenable
from .ILayerListener import ILayerListener
from ..constants.CellValue import CellValue
from core.constants.Direction import Direction


class Layer(Listenable[ILayerListener]):
    """A layer in the game world that can be observed for changes."""
    
    def __init__(self, input_width: int, input_height: int, input_defaultValue: CellValue):
        super().__init__()
        # size of our Layer. Should be immutable.
        self.__width = input_width
        self.__height = input_height
        self.__defaultValue = input_defaultValue
        self.__size = (input_width, input_height)
        # Value of every cell of the Layer. Should be immutable.
        # A 2d matrix - each row has width columns (initialized to default value)
        # and we have height rows
        self.__cells = []
        for y in range(input_height):
            row = [input_defaultValue] * input_width
            self.__cells.append(row)
    
    
    # Getter properties
    @property
    def size(self) -> Tuple[int, int]:
        return self.__size

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def __getitem__(self, coords: Tuple[int, int]) -> CellValue:
        return self.get_cell_value((coords[0], coords[1]))
    
    def __setitem__(self, coords: Tuple[int, int], value: CellValue):
        self.set_cell_value(coords[0],coords[1], value)

    # Getter and Setter for a single cell's value
    def get_cell_value(self, i_coords: Tuple[int, int], i_direction: Optional[Direction] = None) -> int:
        """Get cell value with optional direction parameter"""
        x, y = i_coords[0], i_coords[1]
        if i_direction:
            # Check direction and return the corresponding neighbor's value
            if i_direction == Direction.LEFT:
                if x < 1:
                    return self.__defaultValue
                return self.__cells[y][x - 1]
            if i_direction == Direction.TOP:
                if y < 1:
                    return self.__defaultValue
                return self.__cells[y - 1][x]
            if i_direction == Direction.RIGHT:
                if x >= self.__size[0] - 1:
                    return self.__defaultValue
                return self.__cells[y][x + 1]
            if i_direction == Direction.BOTTOM:
                if y >= self.__size[1] - 1:
                    return self.__defaultValue
                return self.__cells[y + 1][x]
        # Return the value of the cell at the given coordinates
        return self.__cells[y][x]

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

    def getNeighbors4(self, i_cell: Tuple[int, int]) -> Tuple[int, int, int, int]:
        """Get values of 4-connected neighbors (left, top, bottom, right)"""
        x, y = i_cell
        w, h = self.__size[0] - 1, self.__size[1] - 1
        left = self.__cells[y][x - 1] if x > 0 else self.__defaultValue
        top = self.__cells[y - 1][x] if y > 0 else self.__defaultValue
        bottom = self.__cells[y + 1][x] if y < h else self.__defaultValue
        right = self.__cells[y][x + 1] if x < w else self.__defaultValue
        return left, top, bottom, right

    def getNeighbors8(self, i_cell: Tuple[int, int]) -> Tuple[int, int, int, int, int, int, int, int]:
        """Get values of 8-connected neighbors (includes diagonals)"""
        x, y = i_cell
        w, h = self.__size[0] - 1, self.__size[1] - 1
        
        # Get direct neighbors
        left = self.__cells[y][x - 1] if x > 0 else self.__defaultValue
        top = self.__cells[y - 1][x] if y > 0 else self.__defaultValue
        bottom = self.__cells[y + 1][x] if y < h else self.__defaultValue
        right = self.__cells[y][x + 1] if x < w else self.__defaultValue
        
        # Get diagonal neighbors
        top_left = self.__cells[y - 1][x - 1] if x > 0 and y > 0 else self.__defaultValue
        top_right = self.__cells[y - 1][x + 1] if x < w and y > 0 else self.__defaultValue
        bottom_left = self.__cells[y + 1][x - 1] if x > 0 and y < h else self.__defaultValue
        bottom_right = self.__cells[y + 1][x + 1] if x < w and y < h else self.__defaultValue
        
        return (top_left, left, bottom_left, top,
                bottom, top_right, right, bottom_right)
