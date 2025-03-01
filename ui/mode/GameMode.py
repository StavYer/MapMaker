"""
GameMode.py, an abstract class to handle the high-level logics of rendering.
"""

from abc import abstractmethod

from pygame.surface import Surface

from ui.component.CompositeComponent import CompositeComponent
from ui.theme.Theme import Theme

class GameMode(CompositeComponent):
    """Base class for game modes that can contain components"""
    
    @abstractmethod
    def update(self):
        """Update game state"""
        raise NotImplementedError()