import random
from typing import Tuple, Optional

import pygame
from pygame.surface import Surface

from core.constants import CellValue, CellValueRanges
from core.state import World
from core.logic import Logic
from tools.vector import vectorDivI
from ..Mouse import Mouse
from ..theme.Theme import Theme
from .GameMode import GameMode
from ..component.IComponentListener import IComponentListener
from ..component.world.WorldComponent import WorldComponent


class EditGameMode(GameMode, IComponentListener):
    """Game mode for editing the world"""

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme)
        self.__world = i_world
        self.__logic = Logic(i_world)
        self.__font = i_theme.getFont("default")

        # Create world component
        self.__worldComponent = WorldComponent(i_theme, i_world)
        self.addComponent(self.__worldComponent)

        # Set default brush layer
        self.__brushLayer = "ground"

        

    def update(self):
        """Update game state"""
        self.__logic.executeCommands()

    def render(self, i_surface: Surface):
        """Render game mode"""
        super().render(i_surface)

        # Draw UI text
        color = self.theme.getFontColor("default")
        textSurfaces = [
            self.__font.render(message, False, color)
            for message in [
                f"Current brush: {self.__brushLayer}",
                "Click left: add; middle: fill; right: remove",
                "F1/F2/F3: ground/impassable/objects"
            ]
        ]
        y = i_surface.get_height()
        for textSurface in reversed(textSurfaces):
            y -= textSurface.get_height() + 1
            i_surface.blit(textSurface, (0, y))

    # UI Event Handler methods
    def keyDown(self, i_key: int) -> bool:
        """Handle key press"""
        if i_key == pygame.K_F1:
            self.__brushLayer = "ground"
            return True
        elif i_key == pygame.K_F2:
            self.__brushLayer = "impassable"
            return True
        elif i_key == pygame.K_F3:
            self.__brushLayer = "objects"
            return True
        else:
            return super().keyDown(i_key)

    # Component Listener methods
    def __updateCell(self, cell: Tuple[int, int], i_mouse: Mouse):
        """Update cell based on mouse input"""
        if i_mouse.button1 or i_mouse.button2:
            # Add cell value
            if self.__brushLayer == "ground":
                value = CellValue.GROUND_EARTH
            else:
                minValue = CellValueRanges[self.__brushLayer][0]
                maxValue = CellValueRanges[self.__brushLayer][1]
                value = CellValue(random.randint(minValue, maxValue - 1))
            fill = i_mouse.button2
        elif i_mouse.button3:
            # Remove cell value
            if self.__brushLayer == "ground":
                value = CellValue.GROUND_SEA
            else:
                value = CellValue.NONE
            fill = False
        else:
            return

        # Create and add command
        Command = self.__logic.getSetLayerValueCommand(self.__brushLayer)
        command = Command(cell, value, fill)
        self.__logic.addCommand(command)

    def worldCellClicked(self, cell: Tuple[int, int], i_mouse: Mouse):
        """Handle world cell click"""
        self.__updateCell(cell, i_mouse)

    def worldCellEntered(self, cell: Tuple[int, int], i_mouse: Mouse, dragging: bool):
        """Handle mouse entering a world cell"""
        if dragging:
            self.__updateCell(cell, i_mouse)
