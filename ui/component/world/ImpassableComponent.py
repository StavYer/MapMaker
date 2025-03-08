from pygame import Surface

from core.constants import CellValue, Direction, directions
from core.state import World
from tools.tilecodes import mask4, combine4, code4
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
        for dest, value, cell in self.renderedCells(surface):
            if value == CellValue.NONE:
                groundValue = self.__ground.get_cell_value(cell)
                if groundValue == CellValue.GROUND_SEA:
                    for direction in directions:
                        if self.layer.get_cell_value(cell, direction) == CellValue.IMPASSABLE_RIVER:
                            rect = self.__riverMouth[direction]
                            surface.blit(tileset, dest, rect)
            elif value == CellValue.IMPASSABLE_RIVER:
                neighbors = self.layer.getNeighbors4(cell)
                mask = mask4(neighbors, CellValue.IMPASSABLE_RIVER)
                mask = combine4(mask, mask4(neighbors, CellValue.IMPASSABLE_MOUNTAIN))
                neighbors = self.__ground.getNeighbors4(cell)
                mask = combine4(mask, mask4(neighbors, CellValue.GROUND_SEA))
                code = code4(mask)
                rect = self.__river_code2rect[code]
                surface.blit(tileset, dest, rect)
            else:
                rects = tilesRects[value]
                tileCount = len(rects)
                rectIndex = self.noise[cell[1]][cell[0]] % tileCount
                rect = rects[rectIndex]
                surface.blit(tileset, dest, rect)