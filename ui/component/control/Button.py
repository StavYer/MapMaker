from typing import Callable, NoReturn, Tuple

from pygame.surface import Surface

from ui.Mouse import Mouse
from ui.MouseWheel import MouseWheel
from ui.theme.Theme import Theme
from ui.IUIEventHandler import IUIEventHandler
from ui.component.Component import Component

class Button(Component, IUIEventHandler):
    """A button component that triggers an action when clicked."""
    
    def __init__(self, i_theme: Theme, i_surface: Surface, 
                 i_action: Callable[[Mouse], NoReturn]):
        """Initialize with a theme, surface to display, and action to perform."""
        self.__tile = i_surface
        self.__action = i_action
        super().__init__(i_theme, i_surface.get_size())
        
    def render(self, i_surface: Surface):
        """Render the button on the surface."""
        i_surface.blit(self.__tile, self.topLeft)
        
    # UI event handlers (always return True to capture all events in the button area)
    def mouseButtonDown(self, i_mouse: Mouse) -> bool:
        """Handle mouse button down event by triggering the action."""
        self.__action(i_mouse)
        return True
        
    def mouseButtonUp(self, i_mouse: Mouse) -> bool:
        """Handle mouse button up event."""
        return True
        
    def mouseWheel(self, i_mouse: Mouse, i_wheel: MouseWheel) -> bool:
        """Handle mouse wheel event."""
        return True
        
    def mouseMove(self, i_mouse: Mouse) -> bool:
        """Handle mouse move event."""
        return True
        
    def mouseEnter(self, i_mouse: Mouse) -> bool:
        """Handle mouse enter event."""
        return True
        
    def mouseLeave(self) -> bool:
        """Handle mouse leave event."""
        return True