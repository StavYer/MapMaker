import inspect
from itertools import islice

import pygame
from pygame.surface import Surface

from .Component import Component
from .IComponentListener import IComponentListener
from ui.IUIEventHandler import IUIEventHandler

class CacheComponent(Component, IComponentListener, IUIEventHandler):
    """A component that caches the rendering of another component"""
    
    def __init__(self, component: Component):
        super().__init__(component.theme)
        self.__component = component
        self.__surface = None
    
    @property
    def component(self) -> Component:
        return self.__component
    
    # Component interface
    def dispose(self):
        """Clean up resources used by this component"""
        self.__component.dispose()
        self.__surface = None
    
    def needRefresh(self) -> bool:
        """Check if the component needs to be redrawn"""
        return self.__component.needRefresh()
    
    def render(self, surface: Surface):
        """Render the component to the surface, using cache if possible"""
        if self.__surface is None or self.__component.needRefresh():
            self.__surface = Surface(surface.get_size(), flags=pygame.SRCALPHA)
            self.__component.render(self.__surface)
        surface.blit(self.__surface, (0, 0))


# Dynamically create UI event handler methods
eventHandlerMethods = inspect.getmembers(IUIEventHandler, predicate=inspect.isfunction)
for name, method in eventHandlerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CacheComponent_{name}({functionArguments}):
    component = self._CacheComponent__component
    if isinstance(component, IUIEventHandler):
        return component.{name}({methodArguments})
    return False
    '''
    exec(source)
    setattr(CacheComponent, name, locals()['CacheComponent_' + name])

# Dynamically create component listener methods
listenerMethods = inspect.getmembers(IComponentListener, predicate=inspect.isfunction)
for name, method in listenerMethods:
    if name.startswith("__"):
        continue
    signature = inspect.signature(method)
    functionArguments = ", ".join(signature.parameters)
    methodArguments = ", ".join(islice(signature.parameters, 1, None))
    source = f'''
def CacheComponent_{name}({functionArguments}):
    component = self._CacheComponent__component
    if isinstance(component, IComponentListener):
        component.{name}({methodArguments})
    '''
    exec(source)
    setattr(CacheComponent, name, locals()['CacheComponent_' + name])