from abc import ABC, abstractmethod

from pygame import Surface

from ui import Theme


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