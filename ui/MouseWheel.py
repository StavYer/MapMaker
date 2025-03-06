"""
MouseWheel.py, a class for storing mouse wheel data
"""
class MouseWheel:
    """Class representing mouse wheel state"""
    
    def __init__(self, x: float, y: float, flipped: bool, which: int = 0):
        """Initialize a mouse wheel object
        
        Args:
            x: Horizontal scroll amount
            y: Vertical scroll amount
            flipped: Whether scrolling direction is flipped
            which: Which mousewheel was used
        """
        self.__x = x
        self.__y = y
        self.__flipped = flipped
        self.__which = which
    
    @property
    def x(self) -> float:
        """Get horizontal scroll"""
        return self.__x
    
    @property
    def y(self) -> float:
        """Get vertical scroll"""
        return self.__y
    
    @property
    def flipped(self) -> bool:
        """Is scrolling direction flipped"""
        return self.__flipped
    
    @property
    def which(self) -> int:
        """Which mousewheel was used"""
        return self.__which
