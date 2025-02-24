"""
MouseButtons.py, represents mouse button states (left, middle, right) using bitwise operations.
"""

class MouseButtons:

    def __init__(self, i_button1: bool = False, i_button2: bool = False, i_button3: bool = False):
        """Initializes button states using bitwise OR and left shifts."""
        self.buttons = i_button1 | i_button2 << 1 | i_button3 << 2

    @property
    def button1(self) -> bool:
        """Returns True if left button is pressed."""
        return (self.buttons & 1) != 0

    @property
    def button2(self) -> bool:
        """Returns True if middle button is pressed."""
        return (self.buttons & 2) != 0

    @property
    def button3(self) -> bool:
        """Returns True if right button is pressed."""
        return (self.buttons & 4) != 0