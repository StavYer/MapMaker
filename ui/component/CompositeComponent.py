import inspect
from itertools import islice
from typing import List

from pygame.surface import Surface

from .Component import Component
from .IComponentListener import IComponentListener
from ui.IUIEventHandler import IUIEventHandler
from ui.theme.Theme import Theme

class CompositeComponent(Component, IComponentListener, IUIEventHandler):
    """A component that contains and manages other components"""
    
    def __init__(self, theme: Theme):
        super().__init__(theme)
        self.__components: List[Component] = []
    
    def addComponent(self, component: Component, cache: bool = False):
        """Add a component to this composite"""
        if cache:
            # Import here to avoid circular imports
            from .CacheComponent import CacheComponent
            component = CacheComponent(component)
        self.__components.append(component)
    
    def deleteComponents(self):
        """Remove all components from this composite"""
        for component in self.__components:
            component.dispose()
        self.__components.clear()
    
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
    
    def render(self, surface: Surface):
        """Render all components to the surface"""
        for component in self.__components:
            component.render(surface)


# Dynamically create UI event handler methods
eventHandlerMethods = inspect.getmembers(IUIEventHandler, predicate=inspect.isfunction)
for name, method in eventHandlerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CompositeComponent_{name}({functionArguments}):
    for component in reversed(self._CompositeComponent__components):
        if isinstance(component, IUIEventHandler):
            if component.{name}({methodArguments}):
                return True
    return False
    '''
    exec(source)
    setattr(CompositeComponent, name, locals()['CompositeComponent_' + name])

# Dynamically create component listener methods
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
    setattr(CompositeComponent, name, locals()['CompositeComponent_' + name])