# ui/IComponentListener.py
from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .Mouse import Mouse

class IComponentListener(ABC):
    """Interface for objects that want to receive notifications about component events."""
    
    def worldCellClicked(self, i_cell: Tuple[int, int], i_mouse: 'Mouse') -> None:
        """Called when a cell in the world is clicked."""
        pass
    
    def worldCellEntered(self, i_cell: Tuple[int, int], i_mouse: 'Mouse', i_dragging: bool) -> None:
        """Called when mouse enters a cell in the world."""
        pass