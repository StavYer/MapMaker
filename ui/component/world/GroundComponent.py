from pygame import Surface

from core.constants import CellValue
from core.state import World
from tools.tilecodes import mask8, code8
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class GroundComponent(LayerComponent):
    def __init__(self, i_theme: Theme, i_world: World):
        # Initialize the GroundComponent with theme and world
        super().__init__(i_theme, i_world, "ground")
        self.__code2rect = self.tileset.getCode8Rects(0, 0)

    def render(self, i_surface: Surface):
        # Render the ground layer on the given surface
        super().render(i_surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()
        tileWidth, tileHeight = self.tileset.tileSize
        
        # Loop through each cell in the layer
        for y in range(self.layer.height):
            for x in range(self.layer.width):
                value = self.layer[x, y]
                if value == CellValue.NONE:
                    continue  # Skip empty cells
                
                tile = (x * tileWidth, y * tileHeight)
                
                if self.autoTiling:
                    # Auto-tiling logic
                    rects = tilesRects[value]
                    tileCount = len(rects)
                    rectIndex = self.noise[y][x] % tileCount
                    i_surface.blit(tileset, tile, rects[rectIndex])

                    # Add border tiles for sea
                    if value == CellValue.GROUND_SEA:
                        neighbors = self.layer.getNeighbors8((x, y))
                        mask = mask8(neighbors, CellValue.GROUND_SEA)
                        code = code8(mask)
                        rect = self.__code2rect[code]
                        i_surface.blit(tileset, tile, rect)
                else:
                    # Default tiling logic
                    rects = tilesRects[value]
                    i_surface.blit(tileset, tile, rects[0])
