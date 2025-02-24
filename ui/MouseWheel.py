"""
MouseWheel.py, a class for storing mouse wheel data
"""
class MouseWheel:
    def __init__(self, x: int = 0, y: int = 0, flipped: bool = False, which: int = 0):
        # Positions of the mouse wheel events
        self.x = x
        self.y = y
        # If the direction of the mouse wheel is flipped
        self.flipped = flipped
        # Which mouse wheel
        self.which = which
