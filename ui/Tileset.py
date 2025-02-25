from __future__ import annotations  # Enable forward references
from typing import Dict, Tuple, TYPE_CHECKING
from pygame.rect import Rect
from pygame.surface import Surface

# Avoid circular imports
if TYPE_CHECKING:
    from .Theme import Theme

class Tileset:
    """Manages tiles from a sprite sheet image."""
    def __init__(self, theme: Theme, tileSize: Tuple[int, int], imageFile: str):
        """Initialize with theme, tile dimensions, and image file."""
        self.__theme = theme
        self.__tileSize = tileSize
        self.__imageFile = imageFile
        self.__tilesRect: Dict[int, Rect] = {}  # Value to rectangle mapping
    
    @property
    def tileSize(self) -> Tuple[int, int]:
        """Get tile dimensions."""
        return self.__tileSize
    
    def getSurface(self) -> Surface:
        """Get sprite sheet surface."""
        return self.__theme.getSurface(self.__imageFile)
    
    def addTile(self, value: int, coords: Tuple[int, int]):
        """Register a tile at grid coordinates."""
        self.__tilesRect[value] = Rect(
                coords[0] * self.__tileSize[0],  # Grid to pixel conversion
                coords[1] * self.__tileSize[1],
                self.__tileSize[0], self.__tileSize[1]
            )
    
    def getTileRect(self, value: int) -> Rect:
        """Get rectangle for a tile value."""
        if value not in self.__tilesRect:
            raise ValueError(f"No {value} in tileset {self.__imageFile}")
        return self.__tilesRect[value]
    
    def getTilesRect(self) -> Dict[int, Rect]:
        """Get all tile rectangles."""
        return self.__tilesRect