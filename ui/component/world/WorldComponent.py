from typing import Tuple, Optional

from core.state import World
from tools.vector import vectorDivI
from ui.Mouse import Mouse
from ui.theme.Theme import Theme
from ui.IUIEventHandler import IUIEventHandler
from ..CompositeComponent import CompositeComponent
from .LayerComponent import LayerComponent

class WorldComponent(CompositeComponent, IUIEventHandler):
    """Component that renders a world with multiple layers"""
    
    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme)
        self.__world = i_world
        self.__previousCell: Optional[Tuple[int, int]] = None
        self.__mouseButtonDown = False
        
        # Create layer components for each layer in the world
        for name in i_world.layerNames:
            layer = LayerComponent(i_theme, i_world, name)
            self.addComponent(layer, cache=True)
            
        # Get the tile size from the first layer's tileset
        self.__tileSize = i_theme.getTileset(i_world.layerNames[0]).tileSize
    
    def __computeCellCoordinates(self, i_pixel: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to cell coordinates"""
        coords = vectorDivI(i_pixel, self.__tileSize)
        if not self.__world.contains(coords):
            return None
        return coords
    
    # UI Event Handler methods
    def mouseButtonDown(self, i_mouse: Mouse) -> bool:
        """Handle mouse button press"""
        super().mouseButtonDown(i_mouse)
        cell = self.__computeCellCoordinates(i_mouse.coords)
        if cell is None:
            return False
        self.__mouseButtonDown = True
        self.notifyWorldCellClicked(cell, i_mouse)
        return True
    
    def mouseMove(self, i_mouse: Mouse) -> bool:
        """Handle mouse movement"""
        cell = self.__computeCellCoordinates(i_mouse.coords)
        if cell is None:
            self.__previousCell = None
            return False
        if self.__previousCell is not None and cell == self.__previousCell:
            return False
        self.__previousCell = cell
        self.notifyWorldCellEntered(cell, i_mouse, self.__mouseButtonDown)
        return True
    
    def mouseButtonUp(self, i_mouse: Mouse) -> bool:
        """Handle mouse button release"""
        self.__mouseButtonDown = False
        return True
    
    def mouseEnter(self, i_mouse: Mouse) -> bool:
        """Handle mouse entering the component area"""
        self.__mouseButtonDown = False
        return True
    
    def mouseLeave(self) -> bool:
        """Handle mouse leaving the component area"""
        self.__mouseButtonDown = False
        return True