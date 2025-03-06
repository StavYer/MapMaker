# ui/Mouse.py
from typing import Tuple


class Mouse:
    """Class representing mouse state"""
    
    def __init__(self, coords: Tuple[int, int], buttons: Tuple[bool, bool, bool] = (False, False, False)):
        """
        Initialize a mouse object
        
        Args:
            coords: The (x, y) coordinates of the mouse
            buttons: Tuple of (left, middle, right) button states
        """
        self.__coords = coords
        self.__buttons = buttons
    
    @property
    def coords(self) -> Tuple[int, int]:
        """Get mouse coordinates"""
        return self.__coords
    
    @property
    def pixel(self) -> Tuple[int, int]:
        """Get mouse coordinates (alias for backward compatibility)"""
        return self.__coords
    
    @property
    def button1(self) -> bool:
        """Is left button pressed"""
        return self.__buttons[0]
    
    @property
    def button2(self) -> bool:
        """Is middle button pressed"""
        return self.__buttons[1]
    
    @property
    def button3(self) -> bool:
        """Is right button pressed"""
        return self.__buttons[2]
