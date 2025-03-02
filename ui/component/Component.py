from abc import abstractmethod
from typing import List, TYPE_CHECKING

from pygame.surface import Surface

from ui.theme.Theme import Theme
from core.Listenable import Listenable
from ui.component.IComponentListener import IComponentListener

class Component(Listenable[IComponentListener]):
    """Base class for UI components that can be rendered and notify listeners."""
    
    def __init__(self, i_theme: Theme):
        super().__init__()  # Initialize Listenable
        self.__theme = i_theme
        self._needRefresh = True  # Protected attribute for child classes to use
        
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    def dispose(self):
        """Clean up resources when the component is no longer needed."""
        pass
    
    def needRefresh(self) -> bool:
        """Return True if the component needs to be repainted."""
        return self._needRefresh
        
    @abstractmethod
    def render(self, surface: Surface):
        """Render the component to the provided surface."""
        raise NotImplementedError()
    
    # Helper methods to notify listeners
    def notifyWorldCellClicked(self, i_cell: tuple[int, int], i_mouse: 'Mouse') -> None:
        """Notify all listeners that a cell was clicked."""
        for listener in self.listeners:
            listener.worldCellClicked(i_cell, i_mouse)
    
    def notifyWorldCellEntered(self, i_cell: tuple[int, int], i_mouse: 'Mouse', i_dragging: bool) -> None:
        """Notify all listeners that the mouse entered a cell."""
        for listener in self.listeners:
            listener.worldCellEntered(i_cell, i_mouse, i_dragging)