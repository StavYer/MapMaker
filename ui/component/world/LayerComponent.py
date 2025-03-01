"""
    LayerComponent.py renders a specific game world layer using its corresponding tileset.
"""

from pygame import SRCALPHA
from pygame.surface import Surface
from typing import Tuple

from core.constants import CellValue
from core.state import World, Layer, ILayerListener
from .Component import Component
from ui.theme.Theme import Theme


class LayerComponent(Component, ILayerListener):
    """Component that renders a layer and listens for cell changes."""
    
    def __init__(self, i_theme: Theme, i_world: World, i_name: str):
        super().__init__(i_theme)
        # Retrieve the layer and its matching tileset using the given name.
        self.__layer = i_world.getLayer(i_name)
        self.__tileset = i_theme.getTileset(i_name)
        self.__needRefresh = True
        
        # Register as a listener to get notifications about cell changes
        self.__layer.registerListener(self)

    def dispose(self):
        """Remove this component from the layer's listeners when disposed."""
        super().dispose()
        self.__layer.removeListener(self)

    def needRefresh(self) -> bool:
        """Check if the layer needs to be redrawn"""
        return self._needRefresh

    def render(self, i_surface: Surface):
        """Render the layer to the provided surface."""
        # Get the tileset image surface.
        tileset = self.__tileset.getSurface()
        # Retrieve tile dimensions.
        tileWidth, tileHeight = self.__tileset.tileSize
        # Obtain the mapping from cell values to tile rectangles.
        tilesRect = self.__tileset.getTilesRect()
        
        # Iterate over each cell in the layer grid.
        for y in range(self.__layer.height):
            for x in range(self.__layer.width):
                value = self.__layer.get_cell_value(x, y)
                # Skip empty cells.
                if value == CellValue.NONE:
                    continue

                # Get the rectangle area for the current tile value, and calculate the on-screen coordinates for this tile.
                tileRect = tilesRect[value]
                tileCoords = (x * tileWidth, y * tileHeight)

                # Render the tile onto the provided surface.
                i_surface.blit(tileset, tileCoords, tileRect)
                
        # Reset the refresh flag after rendering
        self._needRefresh = False
    
    # ILayerListener implementation
    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        """Called when a cell in a layer changes."""
        if layer == self.__layer:
            self._needRefresh = True  # Mark for refresh when a cell changes
