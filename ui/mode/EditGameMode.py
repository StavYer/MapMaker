import random
from typing import Tuple, Optional

import pygame
from pygame.surface import Surface

from core.constants import CellValue, CellValueRanges
from core.state import World
from ..LayerComponent import LayerComponent
from ..MouseButtons import MouseButtons
from ..Theme import Theme
from .GameMode import GameMode


class EditGameMode(GameMode):

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme)
        self.__world = i_world
        self.__mouseButtonDown = False # True if player clicked inside world
        self.__layers = [
            LayerComponent(i_theme, i_world, name) for name in i_world.layerNames
        ]

        self.__font = i_theme.getFont("default")
        self.__brushLayer = "ground"

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self, i_surface: Surface):
        # Render layers
        for layer in self.__layers:
            layer.render(i_surface)

        # Draw text on surface
        color = self.theme.getFontColor("default")
        textSurfaces = [
            self.__font.render(message, False, color)
            for message in [
               f"Current brush: {self.__brushLayer}",
                "Left click: add",
                "middle click: fill",
                "right click: remove",
                "F1/F2/F3: Select 'ground'/'impassable'/'objects' layer"
            ]
        ]
        y = i_surface.get_height()
        for textSurface in reversed(textSurfaces):
            y -= textSurface.get_height() + 1
            i_surface.blit(textSurface, (0, y))



    # Keyboard handling
    def keyDown(self, i_key: int):
        if i_key == pygame.K_F1:
            self.__brushLayer = "ground"
        elif i_key == pygame.K_F2:
            self.__brushLayer = "impassable"
        elif i_key == pygame.K_F3:
            self.__brushLayer = "objects"


    # Mouse handling

    
    def __computeCellCoordinates(self, i_mouseX: int, i_mouseY: int) -> Optional[Tuple[int, int]]:
        """
        Convert the mouse coordinates from pixels to cells.
        """
        tileWidth, tileHeight = self.theme.getTileset("ground").tileSize
        cellX = i_mouseX // tileWidth
        cellY = i_mouseY // tileHeight

        # If out of render window
        if not (0 <= cellX < self.__world.width) or not (0 <= cellY < self.__world.height):
            return None

        return cellX, cellY

    def __updateCell(self, i_cellX: int, i_cellY: int, i_buttons: MouseButtons):
        
        layer = self.__world.getLayer(self.__brushLayer)
        # update cell based on mouse button (left or right)
        if i_buttons.button1:
            if self.__brushLayer == "ground" and layer.get_cell_value(i_cellX, i_cellY) == CellValue.GROUND_SEA:
                layer.set_cell_value(i_cellX, i_cellY, CellValue.GROUND_EARTH)
            
            elif self.__brushLayer != "ground":
                minValue = CellValueRanges[self.__brushLayer][0]
                maxValue = CellValueRanges[self.__brushLayer][1]
                value = random.randint(minValue, maxValue - 1)
                layer.set_cell_value(i_cellX, i_cellY, CellValue(value))

        elif i_buttons.button3:
            if self.__brushLayer == "ground":
                layer.set_cell_value(i_cellX, i_cellY, CellValue.GROUND_SEA)
            
            else:
                layer.set_cell_value(i_cellX, i_cellY, CellValue.NONE)

    def mouseButtonDown(self, i_mouseX: int, i_mouseY: int, buttons: MouseButtons):
        cellCoordinates = self.__computeCellCoordinates(i_mouseX, i_mouseY)

        # If none, means we are outside render window
        if cellCoordinates is None:
            return

        cellX, cellY = cellCoordinates
        self.__mouseButtonDown = True
        self.__updateCell(cellX, cellY, buttons)

    def mouseMove(self, i_mouseX: int, i_mouseY: int, buttons: MouseButtons):
        if not self.__mouseButtonDown:
            return

        cellCoordinates = self.__computeCellCoordinates(i_mouseX, i_mouseY)

        if cellCoordinates is None:
            return

        cellX, cellY = cellCoordinates
        self.__updateCell(cellX, cellY, buttons)
    
    def mouseButtonUp(self, i_mouseX: int, i_mouseY: int, buttons: MouseButtons):
        self.__mouseButtonDown = False

    def mouseEnter(self, i_mouseX: int, i_mouseY: int, buttons: MouseButtons):
        self.__mouseButtonDown = False

    def mouseLeave(self):
        self.__mouseButtonDown = False
