"""
GameMode.py, an abstract class to handle the high-level logics of rendering.
"""

from abc import ABC, abstractmethod

from pygame.surface import Surface

from ui.Mouse import Mouse
from ui.MouseWheel import MouseWheel
from ui.Theme import Theme

class GameMode(ABC):

    def __init__(self, i_theme: Theme):
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

    # Keyboard handling
    
    def keyDown(self, i_key: int):
        pass

    def keyUp(self, i_key: int):
        pass

    # Mouse handling

    # When mouse enters render area
    def mouseEnter(self, i_mouse: Mouse):
        return False

    # When mouse leaves render area
    def mouseLeave(self):
        return False

    # When mouse button is pressed
    def mouseButtonDown(self, i_mouse: Mouse):
        return False

    # When mouse button is released
    def mouseButtonUp(self, i_mouse: Mouse):
        return False

    # When mouse wheel is scrolled
    def mouseWheel(self, i_mouse: Mouse, i_wheel: MouseWheel):
        return False

    # When mouse moves
    def mouseMove(self, i_mouse: Mouse):
        return False