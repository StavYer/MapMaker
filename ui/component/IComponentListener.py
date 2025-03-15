# ui/IComponentListener.py
from __future__ import annotations
from abc import ABC
from typing import Tuple, Union, Optional, TYPE_CHECKING
from core.constants import UnitClass

if TYPE_CHECKING:
    from ui.Mouse import Mouse

class IComponentListener(ABC):
    """Interface for components that listen to world events"""
    
    def worldCellClicked(self, cell: Tuple[int, int], mouse: Mouse):
        """Called when a cell in the world is clicked"""
        pass

    def worldCellEntered(self, cell: Tuple[int, int], mouse: Mouse, dragging: bool):
        """Called when the mouse enters a cell in the world"""
        pass
    
    def mainBrushSelected(self, layerName: str, value: Union[int, str], unitClass: Optional[UnitClass] = None):
        """Called when the main brush is selected"""
        pass
        
    def secondaryBrushSelected(self, layerName: str, value: Union[int, str], unitClass: Optional[UnitClass] = None):
        """Called when the secondary brush is selected"""
        pass
        
    def viewChanged(self, view: Tuple[int, int]):
        """Called when the view changes"""
        pass
