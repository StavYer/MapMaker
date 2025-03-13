from typing import Tuple, Optional

import numpy as np

from core.constants import CellValue


class LayerRenderer:
    """Renders a layer of cells with view positioning and coordinate transformations."""

    def __init__(self, cells: np.ndarray,
                 cellMinX: int, cellMinY: int, cellMaxX: int, cellMaxY: int,
                 view: Tuple[int, int], tileSize: Tuple[int, int]):
        # Store the cell grid data and rendering parameters
        self.cells = cells
        self.view = view  # Camera position in pixel coordinates
        self.tileSize = tileSize  # Width and height of each tile in pixels
        self.cellsBox = (cellMinX, cellMaxX, cellMinY, cellMaxY)  # Visible cell boundaries
        self.cellsSlice = np.s_[cellMinX:cellMaxX, cellMinY:cellMaxY]  # Slice for visible cells

    def coords(self, validCells: Optional[np.ndarray] = None):
        """Generate rendering coordinates for cells.
        
        Args:
            validCells: Optional mask indicating which cells to render
            
        Yields:
            Tuple containing:
            - (x,y) screen coordinates for drawing
            - Cell value enum
            - (x,y) relative cell position within view
        """
        tileWidth, tileHeight = self.tileSize
        viewX, viewY = self.view
        
        if validCells is None:
            # Render all cells in the visible area
            cells = self.cells
            cellMinX, cellMaxX, cellMinY, cellMaxY = self.cellsBox
            shiftX = cellMinX * tileWidth + viewX % tileWidth
            shiftY = cellMinY * tileHeight + viewY % tileHeight
            
            for cellY in range(cellMinY, cellMaxY):
                for cellX in range(cellMinX, cellMaxX):
                    value = CellValue(cells[cellX, cellY])
                    destX = cellX * tileWidth - shiftX  # Screen x-coordinate 
                    destY = cellY * tileHeight - shiftY  # Screen y-coordinate
                    yield (destX, destY), value, (cellX - cellMinX, cellY - cellMinY)
        else:
            # Render only specified valid cells
            cells = self.cells[self.cellsSlice]
            cellCoords = np.transpose(np.nonzero(validCells))
            
            for cell in cellCoords:
                cellRelX = int(cell[0])
                cellRelY = int(cell[1])
                value = CellValue(cells[cellRelX, cellRelY])
                destX = cellRelX * tileWidth - viewX % tileWidth  # Screen x-coordinate
                destY = cellRelY * tileHeight - viewY % tileHeight  # Screen y-coordinate
                yield (destX, destY), value, (cellRelX, cellRelY)