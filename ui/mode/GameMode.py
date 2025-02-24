from abc import ABC, abstractmethod

from pygame import Surface

from ui import Theme, MouseButtons, MouseWheel


class GameMode(ABC):
    def __init__(self, theme: Theme):
        self.__theme = theme

    @property
    def theme(self):
        return self.__theme

    @abstractmethod
    def processInput(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def render(self, surface: Surface):
        raise NotImplementedError()

    # Mouse handling

    def mouseEnter(self, input_mouseX: int, input_mouseY: int, input_buttons: MouseButtons):
        return False

    def mouseLeave(self):
        return False

    def mouseButtonDown(self, input_mouseX: int, input_mouseY: int, input_buttons: MouseButtons):
        return False

    def mouseButtonUp(self, input_mouseX: int, input_mouseY: int, input_buttons: MouseButtons):
        return False

    def mouseWheel(self, input_mouseX: int, input_mouseY: int, input_buttons: MouseButtons, wheel: MouseWheel):
        return False

    def mouseMove(self, input_mouseX: int, input_mouseY: int, input_buttons: MouseButtons):
        return False