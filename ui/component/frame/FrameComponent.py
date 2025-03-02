from __future__ import annotations

from typing import Optional, Tuple

import pygame
from pygame.surface import Surface

from ui.Mouse import Mouse
from ui.MouseWheel import MouseWheel
from ui.theme.Theme import Theme
from ui.IUIEventHandler import IUIEventHandler
from ui.component.CompositeComponent import CompositeComponent

class FrameComponent(CompositeComponent, IUIEventHandler):
    """A component that displays a frame and can contain other components."""
    
    def __init__(self, i_theme: Theme, i_size: Optional[Tuple[int, int]] = None):
        super().__init__(i_theme, i_size)
        # Get the tileset for frame rendering
        self.__tileset = i_theme.getTileset("frame")
        # Get tile rectangles for each part of the frame
        self.__topLeftTile = self.__tileset.getTileRect("topLeft")
        self.__topTile = self.__tileset.getTileRect("top")
        self.__topRightTile = self.__tileset.getTileRect("topRight")
        self.__leftTile = self.__tileset.getTileRect("left")
        self.__centerTile = self.__tileset.getTileRect("center")
        self.__rightTile = self.__tileset.getTileRect("right")
        self.__bottomLeftTile = self.__tileset.getTileRect("bottomLeft")
        self.__bottomTile = self.__tileset.getTileRect("bottom")
        self.__bottomRightTile = self.__tileset.getTileRect("bottomRight")
        
    def _drawFrame(self, i_surface: Surface, i_dest: Optional[Tuple[int, int]] = None):
        """Draw the frame on the surface."""
        if i_dest is None:
            x1, y1 = self.topLeft
        else:
            x1, y1 = i_dest
        width, height = self.size
        
        # Calculate tile dimensions and frame boundaries
        tileWidth, tileHeight = self.__tileset.tileSize
        x1b = x1 + tileWidth
        x2b = x1 + width - tileWidth
        y1b = y1 + tileHeight
        y2b = y1 + height - tileHeight
        
        # Get tileset surface
        tilesetSurface = self.__tileset.getSurface()
        
        # Draw corners
        i_surface.blit(tilesetSurface, (x1, y1), self.__topLeftTile)
        i_surface.blit(tilesetSurface, (x2b, y1), self.__topRightTile)
        i_surface.blit(tilesetSurface, (x1, y2b), self.__bottomLeftTile)
        i_surface.blit(tilesetSurface, (x2b, y2b), self.__bottomRightTile)
        
        # Draw top and bottom edges
        for x in range(x1b, x2b, tileWidth):
            i_surface.blit(tilesetSurface, (x, y1), self.__topTile)
            i_surface.blit(tilesetSurface, (x, y2b), self.__bottomTile)
            
        # Draw left and right edges
        for y in range(y1b, y2b, tileHeight):
            i_surface.blit(tilesetSurface, (x1, y), self.__leftTile)
            i_surface.blit(tilesetSurface, (x2b, y), self.__rightTile)
            
        # Draw center
        for y in range(y1b, y2b, tileHeight):
            for x in range(x1b, x2b, tileWidth):
                i_surface.blit(tilesetSurface, (x, y), self.__centerTile)
                
    def render(self, i_surface: Surface):
        """Render the frame and its contents."""
        self._drawFrame(i_surface)
        super().render(i_surface)
        
    # UI Event Handler methods - always return True to capture events in the frame area
    
    def mouseEnter(self, i_mouse: Mouse) -> bool:
        """Handle mouse enter event."""
        super().mouseEnter(i_mouse)
        return True
        
    def mouseLeave(self) -> bool:
        """Handle mouse leave event."""
        super().mouseLeave()
        return True
        
    def mouseButtonDown(self, i_mouse: Mouse) -> bool:
        """Handle mouse button down event."""
        super().mouseButtonDown(i_mouse)
        return True
        
    def mouseButtonUp(self, i_mouse: Mouse) -> bool:
        """Handle mouse button up event."""
        super().mouseButtonUp(i_mouse)
        return True
        
    def mouseWheel(self, i_mouse: Mouse, i_wheel: MouseWheel) -> bool:
        """Handle mouse wheel event."""
        super().mouseWheel(i_mouse, i_wheel)
        return True
        
    def mouseMove(self, i_mouse: Mouse) -> bool:
        """Handle mouse move event."""
        super().mouseMove(i_mouse)
        return True