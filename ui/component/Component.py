from __future__ import annotations

from abc import abstractmethod
from typing import Tuple, Optional, Union

from pygame import Surface
from pygame.rect import Rect

from ui.theme.Theme import Theme
from core.Listenable import Listenable
from ui.component.IComponentListener import IComponentListener

class Component(Listenable[IComponentListener]):
    """Base class for UI components that can be rendered and notify listeners."""
    
    def __init__(self, i_theme: Theme, i_size: Optional[Tuple[int, int]] = None):
        super().__init__()  # Initialize Listenable
        self.__theme = i_theme
        self._needRefresh = True  # Protected attribute for child classes to use
        
        # Initialize area
        if i_size is None:
            self.__area = Rect(0, 0, i_theme.viewSize[0], i_theme.viewSize[1])
        else:
            self.__area = Rect(0, 0, i_size[0], i_size[1])
        
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    # Area-related properties
    def contains(self, i_pixel: Tuple[int, int]) -> bool:
        """Check if the pixel is within this component's area."""
        return self.__area.collidepoint(i_pixel) != 0
    
    @property
    def area(self) -> Rect:
        """Get a copy of the component's area."""
        return self.__area.copy()
        
    @property
    def topLeft(self) -> Tuple[int, int]:
        """Get top-left corner coordinates."""
        return int(self.__area.left), int(self.__area.top)
    
    @property
    def topRight(self) -> Tuple[int, int]:
        """Get top-right corner coordinates."""
        return int(self.__area.right), int(self.__area.top)
        
    @property
    def bottomLeft(self) -> Tuple[int, int]:
        """Get bottom-left corner coordinates."""
        return int(self.__area.left), int(self.__area.bottom)
        
    @property
    def bottomRight(self) -> Tuple[int, int]:
        """Get bottom-right corner coordinates."""
        return int(self.__area.right), int(self.__area.bottom)
        
    @property
    def size(self) -> Tuple[int, int]:
        """Get component size."""
        return int(self.__area.width), int(self.__area.height)
    
    def resize(self, i_size: Tuple[int, int]):
        """Resize the component."""
        self.__area.size = i_size
    
    def moveTo(self, i_topLeft: Tuple[int, int]):
        """Move the component to the specified position."""
        self.__area.update(i_topLeft, self.size)
        
    def shiftBy(self, i_shift: Tuple[int, int]):
        """Shift the component by the specified offset."""
        self.__area.move_ip(i_shift)
    
    # Anchor system
    @staticmethod
    def relativeAnchor(i_anchor: str, i_size: Tuple[int, int]) -> Tuple[int, int]:
        """Calculate the relative position of an anchor point in a rectangle."""
        if i_anchor == "topLeft":
            return 0, 0
        elif i_anchor == "top":
            return i_size[0] // 2, 0
        elif i_anchor == "topRight":
            return i_size[0], 0
        elif i_anchor == "left":
            return 0, i_size[1] // 2
        elif i_anchor == "center":
            return i_size[0] // 2, i_size[1] // 2
        elif i_anchor == "right":
            return i_size[0], i_size[1] // 2
        elif i_anchor == "bottomLeft":
            return 0, i_size[1]
        elif i_anchor == "bottom":
            return i_size[0] // 2, i_size[1]
        elif i_anchor == "bottomRight":
            return i_size[0], i_size[1]
        else:
            raise ValueError(f"Invalid anchor {i_anchor}")
            
    @staticmethod
    def innerBorderSize(i_anchor: str, i_borderSize: int) -> Tuple[int, int]:
        """Calculate border size for inner anchoring."""
        if i_anchor == "topLeft":
            return i_borderSize, i_borderSize
        elif i_anchor == "top":
            return 0, i_borderSize
        elif i_anchor == "topRight":
            return -i_borderSize, i_borderSize
        elif i_anchor == "left":
            return i_borderSize, 0
        elif i_anchor == "center":
            return 0, 0
        elif i_anchor == "right":
            return -i_borderSize, 0
        elif i_anchor == "bottomLeft":
            return i_borderSize, -i_borderSize
        elif i_anchor == "bottom":
            return 0, -i_borderSize
        elif i_anchor == "bottomRight":
            return -i_borderSize, -i_borderSize
        else:
            raise ValueError(f"Invalid anchor {i_anchor}")
            
    def moveRelativeTo(self,
                       i_anchor: str,
                       i_other: Optional[Component] = None,
                       i_otherAnchor: str = "center",
                       i_shiftX: Optional[int] = None,
                       i_shiftY: Optional[int] = None,
                       i_borderSize: Optional[int] = None):
        """Position this component relative to another component using anchors."""
        x, y = self.relativeAnchor(i_anchor, self.size)
        if i_other is None:
            otherX, otherY = (0, 0)
            otherWidth, otherHeight = self.theme.viewSize
        else:
            otherX, otherY = i_other.topLeft
            otherWidth, otherHeight = i_other.size
        selfX, selfY = self.relativeAnchor(i_otherAnchor, (otherWidth, otherHeight))
        
        if i_borderSize is None:
            i_borderSize = 4  # Default border size
            
        if i_anchor == i_otherAnchor:
            defaultShiftX, defaultShiftY = self.innerBorderSize(i_anchor, i_borderSize)
            if i_shiftX is None:
                i_shiftX = defaultShiftX
            if i_shiftY is None:
                i_shiftY = defaultShiftY
        else:
            if i_shiftX is None:
                if selfX <= 0:
                    i_shiftX = -i_borderSize
                elif selfX >= otherWidth:
                    i_shiftX = i_borderSize
                else:
                    i_shiftX = 0
                    
            if i_shiftY is None:
                if selfY <= 0:
                    i_shiftY = -i_borderSize
                elif selfY >= otherHeight:
                    i_shiftY = i_borderSize
                else:
                    i_shiftY = 0
                    
        self.moveTo((
            otherX + selfX - x + i_shiftX,
            otherY + selfY - y + i_shiftY
        ))
    
    def dispose(self):
        """Clean up resources when the component is no longer needed."""
        pass
    
    def needRefresh(self) -> bool:
        """Return True if the component needs to be repainted."""
        return self._needRefresh
        
    @abstractmethod
    def render(self, i_surface: Surface):
        """Render the component to the provided surface."""
        raise NotImplementedError()
    
    def findMouseFocus(self, i_mouse: 'Mouse') -> Optional[Component]:
        """Find the component that has mouse focus."""
        from ui.IUIEventHandler import IUIEventHandler
        if not isinstance(self, IUIEventHandler):
            return None
        if not self.contains(i_mouse.coords):
            return None
        return self
    
    # Helper methods to notify listeners
    def notifyWorldCellClicked(self, i_cell: tuple[int, int], i_mouse: 'Mouse') -> None:
        """Notify all listeners that a cell was clicked."""
        for listener in self.listeners:
            listener.worldCellClicked(i_cell, i_mouse)
    
    def notifyWorldCellEntered(self, i_cell: tuple[int, int], i_mouse: 'Mouse', i_dragging: bool) -> None:
        """Notify all listeners that the mouse entered a cell."""
        for listener in self.listeners:
            listener.worldCellEntered(i_cell, i_mouse, i_dragging)
            
    def notifyMainBrushSelected(self, i_layerName: str, i_value: Union(int, str)) -> None:
        """Notify all listeners that the main brush was selected."""
        for listener in self.listeners:
            listener.mainBrushSelected(i_layerName, i_value)
            
    def notifySecondaryBrushSelected(self, i_layerName: str, i_value: Union(int, str)) -> None:
        """Notify all listeners that the secondary brush was selected."""
        for listener in self.listeners:
            listener.secondaryBrushSelected(i_layerName, i_value)

    def notifyViewChanged(self, i_view: tuple[int, int]) -> None:
        """Notify all listeners that the view position has changed."""
        for listener in self.listeners:
            listener.viewChanged(i_view)