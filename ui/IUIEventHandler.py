# ui/IUIEventHandler.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Mouse import Mouse
    from .MouseWheel import MouseWheel

class IUIEventHandler(ABC):
    """Interface for objects that can handle UI events."""
    
    def keyDown(self, i_key: int) -> bool:
        """Called when a key is pressed."""
        return False
    
    def keyUp(self, i_key: int) -> bool:
        """Called when a key is released."""
        return False
    
    def mouseEnter(self, i_mouse: 'Mouse') -> bool:
        """Called when mouse enters the component area."""
        return False
    
    def mouseLeave(self) -> bool:
        """Called when mouse leaves the component area."""
        return False
    
    def mouseButtonDown(self, i_mouse: 'Mouse') -> bool:
        """Called when a mouse button is pressed."""
        return False
    
    def mouseButtonUp(self, i_mouse: 'Mouse') -> bool:
        """Called when a mouse button is released."""
        return False
    
    def mouseWheel(self, i_mouse: 'Mouse', i_wheel: 'MouseWheel') -> bool:
        """Called when mouse wheel is scrolled."""
        return False
    
    def mouseMove(self, i_mouse: 'Mouse') -> bool:
        """Called when mouse is moved."""
        return False