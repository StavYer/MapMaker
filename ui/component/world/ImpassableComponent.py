from pygame import Surface

from core.constants import CellValue
from core.state import World
from ui.theme.Theme import Theme
from .LayerComponent import LayerComponent


class ImpassableComponent(LayerComponent):
    """Component that renders the impassable layer."""
    
    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize with the specific layer name 'impassable'."""
        super().__init__(i_theme, i_world, "impassable")

    def render(self, i_surface: Surface):
        """Render the impassable layer with optional auto-tiling."""
        super().render(i_surface)
        
        tileset = self.tileset.surface
        tilesRect = self.tileset.getTilesRect()
        tileWidth, tileHeight = self.tileset.tileSize
        
        # Render each cell in the layer
        for y in range(self.layer.height):
            for x in range(self.layer.width):
                value = self.layer.get_cell_value(x, y)
                if value == CellValue.NONE:
                    continue
                    
                tileCoords = (x * tileWidth, y * tileHeight)
                
                # Auto-tiling: Select from multiple possible tiles using noise
                if self.autoTiling and value in tilesRect:
                    # Choose tile based on noise value for consistency
                    tileRects = tilesRect[value]
                    if isinstance(tileRects, list):
                        rectIndex = self.noise[y][x] % len(tileRects)
                        tileRect = tileRects[rectIndex]
                    else:
                        tileRect = tileRects
                else:
                    tileRect = tilesRect[value]
                    
                i_surface.blit(tileset, tileCoords, tileRect)