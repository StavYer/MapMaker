from abc import abstractmethod

from pygame.surface import Surface

from ui.theme.Theme import Theme


class Component:
    """Base class for UI components that can be rendered."""
    
    def __init__(self, i_theme: Theme):
        self.__theme = i_theme
        self._needRefresh = True  # Protected attribute for child classes to use
        
    @property
    def theme(self) -> Theme:
        return self.__theme
        
    def dispose(self):
        """Clean up resources when the component is no longer needed."""
        pass
        
    @abstractmethod
    def render(self, surface: Surface):
        """Render the component to the provided surface."""
        raise NotImplementedError()