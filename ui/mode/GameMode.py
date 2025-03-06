"""
GameMode.py, an abstract class to handle the high-level logics of rendering.
"""

from abc import abstractmethod

from ..component.CompositeComponent import CompositeComponent


class GameMode(CompositeComponent):

    def processInput(self):
        pass

    @abstractmethod
    def update(self):
        raise NotImplementedError()



