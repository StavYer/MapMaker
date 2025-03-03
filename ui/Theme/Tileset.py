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
        self.__tilesRects: Dict[Union[int, str], List[Rect]] = {}  # Value to list of rectangles mapping
    
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
        if i_value not in self.__tilesRects:
            self.__tilesRects[i_value] = []
        
        self.__tilesRects[i_value].append(Rect(
            i_coords[0] * self.__tileSize[0],
            i_coords[1] * self.__tileSize[1],
            self.__tileSize[0], self.__tileSize[1]
        ))

    def addTiles(self, i_tilesDefs: Dict[Union[int, str], Union[List[Tuple[int, int]], Tuple[int, int]]]):
        """Add multiple tiles to the tileset.
        """
        for i_value, i_coords in i_tilesDefs.items():
            if isinstance(i_coords, list):
                for i_coord in i_coords:
                    self.addTile(i_value, i_coord)
            elif isinstance(i_coords, tuple):
                self.addTile(i_value, i_coords)
            else:
                raise ValueError(f"Invalid coordinates {i_coords}")

    def getTileRect(self, i_value: Union[int, str]) -> Union[Rect, List[Rect]]:
        """Get rectangle(s) for a tile value."""
        if i_value not in self.__tilesRects:
            raise ValueError(f"No {i_value} in tileset {self.__imageFile}")
        return self.__tilesRects[i_value][0]
    
    def getTileRects(self, i_value: Union[int, str]) -> List[Rect]:
        """Get all rectangles for a specific tile value."""
        if i_value not in self.__tilesRects:
            raise ValueError(f"No {i_value} in tileset {self.__imageFile}")
        return self.__tilesRects[i_value]
    
    def getTile(self, i_value: Union[int, str]) -> Surface:
        """Get a surface for a specific tile."""
        rect = self.getTileRect(i_value)
        surface = Surface(rect.size, flags=pygame.SRCALPHA)
        surface.blit(self.surface, (0, 0), rect)
        return surface
    
    def getTilesId(self) -> List[Union[int, str]]:
        """Get all tile IDs in this tileset."""
        return list(self.__tilesRects.keys())
    
    def getTilesRect(self) -> Dict[Union[int, str], List[Rect]]:
        """Get all tile rectangles."""
        return {value: tileRects[0] for value, tileRects in self.__tilesRects.items()}
    
    