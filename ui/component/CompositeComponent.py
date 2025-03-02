import inspect
from itertools import islice
from typing import List, Optional, Tuple

from pygame.surface import Surface

from .Component import Component
from .IComponentListener import IComponentListener
from ui.IUIEventHandler import IUIEventHandler
from ui.Mouse import Mouse
from ui.theme.Theme import Theme

class CompositeComponent(Component, IComponentListener, IUIEventHandler):
    """A component that contains and manages other components"""
    
    def __init__(self, i_theme: Theme, i_size: Optional[Tuple[int, int]] = None):
        super().__init__(i_theme, i_size)
        self.__components: List[Component] = []
    
    def addComponent(self, i_component: Component, cache: bool = False):
        """Add a component to this composite"""
        if cache:
            # Import here to avoid circular imports
            from .CacheComponent import CacheComponent
            i_component = CacheComponent(i_component)
        self.__components.append(i_component)
    
    def deleteComponents(self):
        """Remove all components from this composite"""
        for component in self.__components:
            component.dispose()
        self.__components.clear()
        
    def moveTo(self, i_topLeft: Tuple[int, int]):
        """Move this component and all children to the specified position."""
        shift = (
            i_topLeft[0] - self.topLeft[0],
            i_topLeft[1] - self.topLeft[1]
        )
        self.shiftBy(shift)
    
    def shiftBy(self, i_shift: Tuple[int, int]):
        """Shift this component and all children by the specified offset."""
        for component in self.__components:
            component.shiftBy(i_shift)
        super().shiftBy(i_shift)
        
    def pack(self):
        """Calculate the minimum area that contains all child components."""
        minX, minY = 10000, 10000
        maxX, maxY = -10000, -10000
        for component in self.__components:
            x1, y1 = component.topLeft
            x2, y2 = component.bottomRight
            minX, minY = min(minX, x1), min(minY, y1)
            maxX, maxY = max(maxX, x2), max(maxY, y2)
            
        borderSize = self.theme.frameBorderSize  # Default border size
        super().moveTo((minX - borderSize, minY - borderSize))
        width = maxX - minX + 2 * borderSize
        height = maxY - minY + 2 * borderSize
        super().resize((width, height))
    
    # Component interface
    def dispose(self):
        """Clean up resources used by this component"""
        for component in self.__components:
            component.dispose()
    
    def needRefresh(self) -> bool:
        """Check if any component needs to be redrawn"""
        for component in self.__components:
            if component.needRefresh():
                return True
        return False
    
    def render(self, i_surface: Surface):
        """Render all components to the surface"""
        for component in self.__components:
            component.render(i_surface)
            
    # Mouse event handling
    def findMouseFocus(self, i_mouse: Mouse) -> Optional[Component]:
        """Find the component that has mouse focus."""
        for component in reversed(self.__components):
            if not isinstance(component, IUIEventHandler):
                continue
            childFocus = component.findMouseFocus(i_mouse)
            if childFocus is not None:
                return childFocus
        return super().findMouseFocus(i_mouse)
        
    def mouseButtonDown(self, i_mouse: Mouse) -> bool:
        """Handle mouse button down event."""
        for component in reversed(self.__components):
            if not component.contains(i_mouse.coords):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseButtonDown(i_mouse):
                return True
        return False
        
    def mouseButtonUp(self, i_mouse: Mouse) -> bool:
        """Handle mouse button up event."""
        for component in reversed(self.__components):
            if not component.contains(i_mouse.coords):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseButtonUp(i_mouse):
                return True
        return False
        
    def mouseWheel(self, i_mouse: Mouse, i_wheel: 'MouseWheel') -> bool:
        """Handle mouse wheel event."""
        for component in reversed(self.__components):
            if not component.contains(i_mouse.coords):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseWheel(i_mouse, i_wheel):
                return True
        return False
        
    def mouseMove(self, i_mouse: Mouse) -> bool:
        """Handle mouse move event."""
        for component in reversed(self.__components):
            if not component.contains(i_mouse.coords):
                continue
            if not isinstance(component, IUIEventHandler):
                continue
            if component.mouseMove(i_mouse):
                return True
        return False

# Dynamic creation of Component listener methods
listenerMethods = inspect.getmembers(IComponentListener, predicate=inspect.isfunction)
for name, method in listenerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CompositeComponent_{name}({functionArguments}):
    for component in reversed(self._CompositeComponent__components):
        if isinstance(component, IComponentListener):
            component.{name}({methodArguments})
    '''
    exec(source)
    setattr(CompositeComponent, name, globals()['CompositeComponent_' + name])