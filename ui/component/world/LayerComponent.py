"""
LayerComponent.py renders a specific game world layer using its corresponding tileset.
"""

import random
from pygame import SRCALPHA
from pygame.surface import Surface
from typing import Tuple, List, Optional

from core.constants import CellValue
from core.state import World, Layer, ILayerListener
from ..Component import Component
from ui.theme.Theme import Theme
from ui.theme.Tileset import Tileset


class LayerComponent(Component, ILayerListener):
    """Component that renders a layer and listens for cell changes."""
    
    def __init__(self, i_theme: Theme, i_world: World, i_name: str):
        """Initialize the component with a specific layer from the world."""
        super().__init__(i_theme)
        # Retrieve the layer and its matching tileset using the given name
        self.__layer = i_world.getLayer(i_name)
        self.__tileset = i_theme.getTileset(i_name)
        self.__needRefresh = True
        self.__autoTiling = True
        
        # Register as a listener to get notifications about cell changes
        self.__layer.registerListener(self)
        
        # Generate noise for random tile selection
        random.seed(i_name)  # Use consistent seed based on layer name
        self.__noise = []
        width, height = self.__layer.width, self.__layer.height
        for y in range(height):
            row = []
            for x in range(width):
                row.append(random.randint(0, 100000))
            self.__noise.append(row)

    def dispose(self):
        """Remove this component from the layer's listeners when disposed."""
        super().dispose()
        self.__layer.removeListener(self)

    @property
    def layer(self) -> Layer:
        """Get the layer being rendered."""
        return self.__layer
        
    @property
    def tileset(self) -> Tileset:
        """Get the tileset used for rendering."""
        return self.__tileset
        
    @property
    def noise(self) -> List[List[int]]:
        """Get the noise array used for random tile selection."""
        return self.__noise
        
    @property
    def autoTiling(self) -> bool:
        """Check if auto-tiling is enabled."""
        return self.__autoTiling
        
    @autoTiling.setter
    def autoTiling(self, i_value: bool):
        """Set auto-tiling mode and mark for refresh."""
        self.__autoTiling = i_value
        self.__needRefresh = True

    def needRefresh(self) -> bool:
        """Check if the layer needs to be redrawn."""
        return self.__needRefresh

    def render(self, i_surface: Surface):
        """Base render method, to be overridden by subclasses."""
        # Mark as rendered
        self.__needRefresh = False
        
    # ILayerListener implementation
    def cellChanged(self, layer: Layer, cell: Tuple[int, int]):
        """Called when a cell in a layer changes."""
        if layer == self.__layer:
            self.__needRefresh = True  # Mark for refresh when a cell changes
