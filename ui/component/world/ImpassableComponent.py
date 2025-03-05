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

    def render(self, i_surface: Surface):
        """Render the impassable terrain features on the given surface"""
        super().render(i_surface)
        i_tileset = self.tileset.surface
        i_tilesRects = self.tileset.getTilesRects()
        i_tileWidth, i_tileHeight = self.tileset.tileSize
        
        # Iterate over each cell in the layer
        for i_y in range(self.layer.height):
            for i_x in range(self.layer.width):
                i_value = self.layer[i_x, i_y]
                i_tile = (i_x * i_tileWidth, i_y * i_tileHeight)
                
                if self.autoTiling:
                    if i_value == CellValue.NONE:
                        # Check for sea connections in the ground layer
                        i_groundValue = self.__ground.get_cell_value((i_x, i_y))
                        if i_groundValue == CellValue.GROUND_SEA:
                            for i_direction in directions:
                                if self.layer.get_cell_value((i_x, i_y), i_direction) == CellValue.IMPASSABLE_RIVER:
                                    i_rect = self.__riverMouth[i_direction]
                                    i_surface.blit(i_tileset, i_tile, i_rect)
                    elif i_value == CellValue.IMPASSABLE_RIVER:
                        # Determine the appropriate river tile based on neighbors
                        i_neighbors = self.layer.getNeighbors4((i_x, i_y))
                        i_mask = mask4(i_neighbors, CellValue.IMPASSABLE_RIVER)
                        i_mask = combine4(i_mask, mask4(i_neighbors, CellValue.IMPASSABLE_MOUNTAIN))
                        i_neighbors = self.__ground.getNeighbors4((i_x, i_y))
                        i_mask = combine4(i_mask, mask4(i_neighbors, CellValue.GROUND_SEA))
                        i_code = code4(i_mask)
                        i_rect = self.__river_code2rect[i_code]
                        i_surface.blit(i_tileset, i_tile, i_rect)
                    else:
                        # Render other impassable features
                        i_rects = i_tilesRects[i_value]
                        i_tileCount = len(i_rects)
                        i_rectIndex = self.noise[i_y][i_x] % i_tileCount
                        i_rect = i_rects[i_rectIndex]
                        i_surface.blit(i_tileset, i_tile, i_rect)
                elif i_value != CellValue.NONE:
                    # Render non-auto-tiling impassable features
                    i_rects = i_tilesRects[i_value]
                    i_surface.blit(i_tileset, i_tile, i_rects[0])