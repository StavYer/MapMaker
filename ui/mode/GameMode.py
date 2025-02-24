"""
GameMode.py, an abstract class to handle the high-level logics of rendering.
"""

from abc import abc, abstractmethod

from pygame.surface import Surface

from ui.MouseButtons import MouseButtons
from ui.MouseWheel import MouseWheel
from ui.Theme import Theme

class GameMode(ABC):

    def __init__(self, i_theme: Theme)
        self.__theme = i_theme

    @property
    def theme(self) -> Theme:
        return self.__theme
    
    @abstractmethod
    def processInput(self):
        raise NotImplementedError()
    
    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def render(self, i_surface: Surface):
        raise NotImplementedError()

    # Mouse handling

    # When mouse enters render area
    def mouseEnter(self, i_mouseX: int, i_mouseY: int, i_buttons: MouseButtons):
        return False

    # When mouse leaves render area
    def mouseLeave(self):
        return False

    # When mouse button is pressed
    def mouseButtonDown(self, i_mouseX: int, i_mouseY: int, i_buttons: MouseButtons):
        return False

    # When mouse button is released
    def mouseButtonUp(self, i_mouseX: int, i_mouseY: int, i_buttons: MouseButtons):
        return False

    # When mouse wheel is scrolled
    def mouseWheel(self, i_mouseX: int, i_mouseY: int, i_buttons: MouseButtons, i_wheel: MouseWheel):
        return False

    # When mouse moves
    def mouseMove(self, i_mouseX: int, i_mouseY: int, i_buttons: MouseButtons):
        return False