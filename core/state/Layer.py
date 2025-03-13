# core/state/Layer.py
from typing import Tuple, Optional

import numpy as np

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
        # Create array with 1-cell border all around for easier neighbor access
        self.__cells = np.full([input_width+2, input_height+2], input_defaultValue, dtype=np.int32)
    
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

    @property
    def cells(self) -> np.ndarray:
        """Get the inner cells without border."""
        return self.__cells[1:-1, 1:-1]

    def __getitem__(self, coords: Tuple[int, int]) -> CellValue:
        return self.get_cell_value((coords[0], coords[1]))
    
    def __setitem__(self, coords: Tuple[int, int], value: CellValue):
        self.set_cell_value(coords[0],coords[1], value)

    # Getter and Setter for a single cell's value
    def get_cell_value(self, i_coords: Tuple[int, int], i_direction: Optional[Direction] = None) -> int:
        """Get cell value with optional direction parameter"""
        x, y = i_coords[0], i_coords[1]
        assert 0 <= x < self.__width, f"invalid cell x coordinate: {x}"
        assert 0 <= y < self.__height, f"invalid cell y coordinate: {y}"
        if i_direction:
            # Check direction and return the corresponding neighbor's value
            if i_direction == Direction.LEFT:
                return CellValue(self.__cells[x, y + 1])
            if i_direction == Direction.TOP:
                return CellValue(self.__cells[x + 1, y])
            if i_direction == Direction.RIGHT:
                return CellValue(self.__cells[x + 2, y + 1])
            if i_direction == Direction.BOTTOM:
                return CellValue(self.__cells[x + 1, y + 2])
        # Return the value of the cell at the given coordinates (offset by border)
        return CellValue(self.__cells[x + 1, y + 1])

    def set_cell_value(self, input_x: int, input_y: int, value: CellValue) -> None:
        # Same here
        assert 0 <= input_x < self.__width, f"invalid cell x coordinate: {input_x}"
        assert 0 <= input_y < self.__height, f"invalid cell y coordinate: {input_y}"
        self.__cells[input_x + 1, input_y + 1] = value
    
  
    # Layer listener notification method
    def notifyCellChanged(self, cell: Tuple[int, int]):
        """Notify all listeners that a cell has changed."""
        for listener in self.listeners:
            listener.cellChanged(self, cell)

    def getNeighbors4(self, cell: Tuple[int, int]) -> Tuple[int, int, int, int]:
        x, y = cell
        return CellValue(self.__cells[x, y + 1]), \
               CellValue(self.__cells[x + 1, y]), \
               CellValue(self.__cells[x + 1, y + 2]), \
               CellValue(self.__cells[x + 2, y + 1])

    def getAllNeighbors4(self) -> np.ndarray:
        w, h = self.__size
        top = self.__cells[1:w + 1, 0:h]
        left = self.__cells[0:w, 1:h + 1]
        right = self.__cells[2:w + 2, 1:h + 1]
        bottom = self.__cells[1:w + 1, 2:h + 2]
        return np.stack((left, top, bottom, right), axis=2)

    def getAreaNeighbors4(self, cellsBox: Tuple[int, int, int, int]) -> np.ndarray:
        minX, maxX, minY, maxY = cellsBox
        top = self.__cells[minX + 1:maxX + 1, minY:maxY]
        left = self.__cells[minX:maxX, minY + 1:maxY + 1]
        right = self.__cells[minX + 2:maxX + 2, minY + 1:maxY + 1]
        bottom = self.__cells[minX + 1:maxX + 1, minY + 2:maxY + 2]
        return np.stack((left, top, bottom, right), axis=2)

    def getNeighbors8(self, cell: Tuple[int, int]) -> Tuple[int, int, int, int, int, int, int, int]:
        x, y = cell
        n = np.delete(self.__cells[x:x + 3, y:y + 3].flatten(), 4)
        return CellValue(n[0]), CellValue(n[1]), CellValue(n[2]), CellValue(n[3]), \
               CellValue(n[4]), CellValue(n[5]), CellValue(n[6]), CellValue(n[7])

    def getAreaNeighbors8(self, cellsBox: Tuple[int, int, int, int]) -> np.ndarray:
        minX, maxX, minY, maxY = cellsBox
        topLeft = self.__cells[minX:maxX, minY:maxY]
        top = self.__cells[minX + 1:maxX + 1, minY:maxY]
        topRight = self.__cells[minX + 2:maxX + 2, minY:maxY]
        left = self.__cells[minX:maxX, minY + 1:maxY + 1]
        right = self.__cells[minX + 2:maxX + 2, minY + 1:maxY + 1]
        bottomLeft = self.__cells[minX:maxX, minY + 2:maxY + 2]
        bottom = self.__cells[minX + 1:maxX + 1, minY + 2:maxY + 2]
        bottomRight = self.__cells[minX + 2:maxX + 2, minY + 2:maxY + 2]
        return np.stack((topLeft, left, bottomLeft, top,
                         bottom, topRight, right, bottomRight), axis=2)

    def getAllNeighbors8(self) -> np.ndarray:
        w, h = self.__size
        topLeft = self.__cells[0:w, 0:h]
        top = self.__cells[1:w + 1, 0:h]
        topRight = self.__cells[2:w + 2, 0:h]
        left = self.__cells[0:w, 1:h + 1]
        right = self.__cells[2:w + 2, 1:h + 1]
        bottomLeft = self.__cells[0:w, 2:h + 2]
        bottom = self.__cells[1:w + 1, 2:h + 2]
        bottomRight = self.__cells[2:w + 2, 2:h + 2]
        return np.stack((topLeft, left, bottomLeft, top,
                         bottom, topRight, right, bottomRight), axis=2)
