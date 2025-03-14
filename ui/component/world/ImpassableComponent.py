import numpy as np
from pygame import Surface

from core.constants import CellValue, Direction, directions
from core.state import World
from tools.tilecodes import code4np
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ImpassableComponent(LayerComponent):
    """Component that renders impassable terrain features"""

    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize the impassable layer renderer"""
        super().__init__(i_theme, i_world, "impassable")
# Get the ground layer to check for sea connections
        self.__ground = i_world.getLayer("ground")
        # Get lookup table for 4-connected river tiles
        self.__river_code2rect = self.tileset.getCode4Rects(0, 1)
        # Get river mouth tiles (where rivers connect to sea)
        self.__riverMouth = {
            Direction.LEFT: self.tileset.getTileRect("riverMouthLeft"),
            Direction.RIGHT: self.tileset.getTileRect("riverMouthRight"),
            Direction.TOP: self.tileset.getTileRect("riverMouthTop"),
            Direction.BOTTOM: self.tileset.getTileRect("riverMouthBottom"),
        }

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox
        cells = self.layer.cells[cellsSlice]

        # Default
        valid = cells != CellValue.NONE
        valid &= cells != CellValue.IMPASSABLE_RIVER
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.coords(valid):
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Rivers
        neighbors = self.layer.getAreaNeighbors4(cellsBox)
        masks = neighbors == CellValue.IMPASSABLE_RIVER
        masks |= neighbors == CellValue.IMPASSABLE_MOUNTAIN
        groundNeighbors = self.__ground.getAreaNeighbors4(cellsBox)
        masks |= groundNeighbors == CellValue.GROUND_SEA
        codes = code4np(masks)

        valid = cells == CellValue.IMPASSABLE_RIVER
        for dest, value, cell in renderer.coords(valid):
            rect = self.__river_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # River mouths
        groundCells = self.__ground.cells[cellsSlice]
        valid = cells == CellValue.NONE
        valid &= groundCells == CellValue.GROUND_SEA
        codes = code4np(neighbors == CellValue.IMPASSABLE_RIVER)
        valid &= codes != 0
        cellMinX, _, cellMinY, _ = renderer.cellsBox
        for dest, _, cell in renderer.coords(valid):
            for direction in directions:
                cellX, cellY = cellMinX + cell[0], cellMinY + cell[1]
                value = self.layer.get_cell_value((cellX, cellY), direction)
                if value == CellValue.IMPASSABLE_RIVER:
                    rect = self.__riverMouth[direction]
                    surface.blit(tileset, dest, rect)