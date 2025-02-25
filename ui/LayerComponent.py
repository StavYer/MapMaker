"""
    LayerComponent.py renders a specific game world layer using its corresponding tileset.

    This component retrieves a layer from the world and the matching tileset from the theme.
    It iterates over the grid cells of the layer, rendering non-empty tiles onto the target surface.
"""

from pygame import SRCALPHA  # Import flag for surfaces supporting per-pixel alpha.
from pygame.surface import Surface
from typing import Tuple, Optional

from core.constants import CellValue
from core.state import World, Layer
from ui.theme.Theme import Theme


class LayerComponent:
    def __init__(self, i_theme: Theme, i_world: World, i_name: str):
        # Retrieve the layer and its matching tileset using the given name.
        self.__layer = i_world.getLayer(name)
        self.__tileset = theme.getTileset(name)

    def render(self, i_surface: Surface):
        # Create a temporary transparent surface matching the target surface size.
        self.__surface = Surface(i_surface.get_size(), flags=SRCALPHA)
        # Get the tileset image surface.
        tileset = self.__tileset.getSurface()
        # Retrieve tile dimensions.
        tileWidth, tileHeight = self.__tileset.tileSize
        # Obtain the mapping from cell values to tile rectangles.
        tilesRect = self.__tileset.getTilesRect()
        # Iterate over each cell in the layer grid.
        for y in range(self.__layer.height):
            for x in range(self.__layer.width):
                value = self.__layer[x, y]
                # Skip empty cells.
                if value == CellValue.NONE:
                    continue

                # Get the rectangle area for the current tile value, and calculate the on-screen coordinates for this tile.
                tileRect = tilesRect[value]
                tileCoords = (x * tileWidth, y * tileHeight)

                # Render the tile onto the provided surface.
                i_surface.blit(tileset, tileCoords, tileRect)
