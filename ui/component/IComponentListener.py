# ui/IComponentListener.py
from abc import ABC
from typing import Tuple, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ui.Mouse import Mouse

class IComponentListener(ABC):
    """Interface for objects that want to receive notifications about component events."""
    
    def worldCellClicked(self, i_cell: Tuple[int, int], i_mouse: 'Mouse') -> None:
        """Called when a cell in the world is clicked."""
        pass
    
    def worldCellEntered(self, i_cell: Tuple[int, int], i_mouse: 'Mouse', i_dragging: bool) -> None:
        """Called when mouse enters a cell in the world."""
        pass
        
    def mainBrushSelected(self, i_layerName: str, i_value: Union[int, str]) -> None:
        """Called when the main brush is selected."""
        pass
        
    def secondaryBrushSelected(self, i_layerName: str, i_value: Union[int, str]) -> None:
        """Called when the secondary brush is selected."""
        pass
        
    def viewChanged(self, i_view: Tuple[int, int]) -> None:
        """Called when the view position changes."""
        pass
