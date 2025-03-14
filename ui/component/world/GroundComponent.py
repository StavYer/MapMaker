from pygame import Surface
import numpy as np

from core.constants import CellValue
from core.state import World
from tools.tilecodes import code8np
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class GroundComponent(LayerComponent):
    def __init__(self, i_theme: Theme, i_world: World):
        # Initialize the GroundComponent with theme and world
        super().__init__(i_theme, i_world, "ground")
        self.__code2rect = self.tileset.getCode8Rects(0, 0)

    def render(self, surface: Surface):
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellsBox = renderer.cellsBox

        # Ground / Sea
        noise = self.noise[cellsSlice]
        for dest, value, cell in renderer.coords():
            rects = tilesRects[value]
            rectIndex = int(noise[cell]) % len(rects)
            surface.blit(tileset, dest, rects[rectIndex])

        # Sea borders
        neighbors = self.layer.getAreaNeighbors8(cellsBox)
        masks = neighbors == CellValue.GROUND_SEA
        codes = code8np(masks)

        cells = self.layer.cells[cellsSlice]
        valid = cells == CellValue.GROUND_SEA
        valid &= codes != 255
        for dest, value, cell in renderer.coords(valid):
            rect = self.__code2rect[codes[cell]]
            surface.blit(tileset, dest, rect)