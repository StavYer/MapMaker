from __future__ import annotations  # Enable forward references
from typing import Dict, Tuple, TYPE_CHECKING, Union, Optional, List
import pygame
from pygame.rect import Rect
from pygame.surface import Surface

# Avoid circular imports
if TYPE_CHECKING:
    from .Theme import Theme

class Tileset:
    """Manages tiles from a sprite sheet image."""
    def __init__(self, i_theme: Theme, i_tileSize: Tuple[int, int], i_imageFile: str):
        """Initialize with theme, tile dimensions, and image file."""
        self.__theme = i_theme
        self.__tileSize = i_tileSize
        self.__imageFile = i_imageFile
        self.__surface: Optional[Surface] = None
        self.__tilesRect: Dict[Union[int, str], Rect] = {}  # Value to rectangle mapping
    
    @property
    def tileSize(self) -> Tuple[int, int]:
        """Get tile dimensions."""
        return self.__tileSize
    
    @property
    def surface(self) -> Surface:
        """Get sprite sheet surface."""
        if self.__surface is None:
            self.__surface = self.__theme.getSurface(self.__imageFile)
        return self.__surface
    
    def addTile(self, i_value: Union[int, str], i_coords: Tuple[int, int]):
        """Register a tile at grid coordinates."""
        self.__tilesRect[i_value] = Rect(
                i_coords[0] * self.__tileSize[0],  # Grid to pixel conversion
                i_coords[1] * self.__tileSize[1],
                self.__tileSize[0], self.__tileSize[1]
            )
    
    def getTileRect(self, i_value: Union[int, str]) -> Rect:
        """Get rectangle for a tile value."""
        if i_value not in self.__tilesRect:
            raise ValueError(f"No {i_value} in tileset {self.__imageFile}")
        return self.__tilesRect[i_value]
    
    def getTile(self, i_value: Union[int, str]) -> Surface:
        """Get a surface for a specific tile."""
        rect = self.getTileRect(i_value)
        surface = Surface(rect.size, flags=pygame.SRCALPHA)
        surface.blit(self.surface, (0, 0), rect)
        return surface
    
    def getTilesId(self) -> List[Union[int, str]]:
        """Get all tile IDs in this tileset."""
        return list(self.__tilesRect.keys())
    
    def getTilesRect(self) -> Dict[Union[int, str], Rect]:
        """Get all tile rectangles."""
        return self.__tilesRect