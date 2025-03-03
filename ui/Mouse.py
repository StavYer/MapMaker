# ui/Mouse.py
from typing import Tuple, Union

class Mouse:
    def __init__(self, coords: Tuple[int, int], buttons: Union[Tuple[bool, bool, bool], Tuple[bool, bool, bool, bool, bool]] = (False, False, False)):
        # Initialize the Mouse object with coordinates and button states.
        self.coords = coords
        self.buttons = buttons

    @property
    def x(self) -> int:
    # Get the x-coordinate of the mouse.
        return self.coords[0]

    @property
    def y(self) -> int:
        # Get the y-coordinate of the mouse.
        return self.coords[1]

    @property
    def button1(self) -> bool:
        # Get the state of the first mouse button.
        return self.buttons[0]

    @property
    def button2(self) -> bool:
        # Get the state of the second mouse button.
        return self.buttons[1]

    @property
    def button3(self) -> bool:
        # Get the state of the third mouse button.
        return self.buttons[2]
