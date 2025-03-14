import numpy as np
from pygame import Surface

from core.constants import CellValue, Direction
from core.state import World
from tools.tilecodes import mask4, combine4, code4, code4np
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ObjectsComponent(LayerComponent):
    """Component that renders object features like roads, buildings"""
    
    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize with theme and world reference"""
        super().__init__(i_theme, i_world, "objects")
        # Get the impassable layer to check for rivers under bridges
        self.__impassableLayer = i_world.getLayer("impassable")
        # Get bridge tile rectangles
        self.__bridgeDirtRects = self.tileset.getTileRects("bridgeDirt")
        self.__bridgeStoneRects = self.tileset.getTileRects("bridgeStone")

        self.__horizontalBrigdes = {
            CellValue.OBJECTS_ROAD_DIRT: self.__bridgeDirtRects[0],
            CellValue.OBJECTS_ROAD_STONE: self.__bridgeStoneRects[0],
        }
        self.__verticalBrigdes = {
            CellValue.OBJECTS_ROAD_DIRT: self.__bridgeDirtRects[1],
            CellValue.OBJECTS_ROAD_STONE: self.__bridgeStoneRects[1],
        }
        # Get lookup tables for road tiles
        self.__roadDirt_code2rect = self.tileset.getCode4Rects(0, 3)
        self.__roadStone_code2rect = self.tileset.getCode4Rects(4, 3)

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox
        cells = self.layer.cells[cellsSlice]
        impassableCells = self.__impassableLayer.cells[cellsSlice]

        # Default
        valid = cells != CellValue.NONE
        valid &= cells != CellValue.OBJECTS_ROAD_DIRT
        valid &= cells != CellValue.OBJECTS_ROAD_STONE
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.coords(valid):
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Road border codes
        neighbors = self.layer.getAreaNeighbors4(cellsBox)
        masks = neighbors == CellValue.OBJECTS_ROAD_DIRT
        masks |= neighbors == CellValue.OBJECTS_ROAD_STONE
        codes = code4np(masks)

        # Dirt roads (without bridges)
        valid = cells == CellValue.OBJECTS_ROAD_DIRT
        valid &= impassableCells != CellValue.IMPASSABLE_RIVER
        for dest, value, cell in renderer.coords(valid):
            rect = self.__roadDirt_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # Stone roads (without bridges)
        valid = cells == CellValue.OBJECTS_ROAD_STONE
        valid &= impassableCells != CellValue.IMPASSABLE_RIVER
        for dest, value, cell in renderer.coords(valid):
            rect = self.__roadStone_code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)

        # River codes
        neighbors = self.__impassableLayer.getAreaNeighbors4(cellsBox)
        codes = code4np(neighbors == CellValue.IMPASSABLE_RIVER)

        # Cells with a road and a river
        valid = cells == CellValue.OBJECTS_ROAD_DIRT
        valid |= cells == CellValue.OBJECTS_ROAD_STONE
        valid &= impassableCells == CellValue.IMPASSABLE_RIVER

        # Horizontal bridges
        horizontal = valid & (codes == 6)
        for dest, value, cell in renderer.coords(horizontal):
            rect = self.__horizontalBrigdes[value]
            surface.blit(tileset, dest, rect)

        # Vertical bridges
        horizontal = valid & (codes == 9)
        for dest, value, cell in renderer.coords(horizontal):
            rect = self.__verticalBrigdes[value]
            surface.blit(tileset, dest, rect)