import pygame
from pygame.surface import Surface

from .Component import Component


class CacheComponent(Component):
    """A proxy component that caches the rendering of another component."""
    
    def __init__(self, i_component: Component):
        super().__init__(component.theme)
        self.__component = i_component
        self.__surface = None
        
    @property
    def component(self) -> Component:
        return self.__component
        
    def dispose(self):
        """Dispose both the cache and the wrapped component."""
        self.__component.dispose()
        self.__surface = None
        
    def render(self, i_surface: Surface):
        """Render using a cached surface if possible."""
        # Only re-render if needed (first time or component needs refresh)
        if self.__surface is None or self.__component._needRefresh:
            # Create a surface with alpha channel
            self.__surface = Surface(i_surface.get_size(), flags=pygame.SRCALPHA)
            # Render the underlying component to our cache
            self.__component.render(self.__surface)
            
        # Blit the cached surface to the target
        i_surface.blit(self.__surface, (0, 0))