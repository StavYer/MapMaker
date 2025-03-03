from pygame import Surface

from core.constants import CellValue
from core.state import World
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ObjectsComponent(LayerComponent):
    def __init__(self, i_theme: Theme, i_world: World):
        # Initialize the parent class with theme, world, and layer name "objects"
        super().__init__(i_theme, i_world, "objects")
        # Get the impassable layer from the world
        self.__impassableLayer = i_world.getLayer("impassable")

    def render(self, i_surface: Surface):
        # Call the parent class render method
        super().render(i_surface)
        # Get the tileset surface and tile rectangles
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()
        tileWidth, tileHeight = self.tileset.tileSize
        
        # Loop through each cell in the layer
        for y in range(self.layer.height):
            for x in range(self.layer.width):
                value = self.layer[x, y]
                # Skip if the cell value is NONE
                if value == CellValue.NONE:
                    continue
                tile = (x * tileWidth, y * tileHeight)
                # Determine the rectangle to use for the tile
                if self.autoTiling:
                    rects = tilesRects[value]
                    tileCount = len(rects)
                    rectIndex = self.noise[y][x] % tileCount
                    rect = rects[rectIndex]
                else:
                    rect = tilesRects[value][0]
                # Draw the tile on the surface
                i_surface.blit(tileset, tile, rect)

