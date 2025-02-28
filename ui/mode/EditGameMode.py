import random
from typing import Tuple, Optional

import pygame
from pygame.surface import Surface

from core.constants import CellValue, CellValueRanges
from core.state import World
from core.logic import Logic
from tools.vector import vectorDivI
from ..LayerComponent import LayerComponent
from ..Mouse import Mouse
from ..Theme import Theme
from .GameMode import GameMode
from ..LayerComponent import LayerComponent
from ..CacheComponent import CacheComponent


class EditGameMode(GameMode):

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme)
        self.__world = i_world
        self.__logic = Logic(i_world)
        self.__mouseButtonDown = False # True if player clicked inside world
        self.__layers = [
            CacheComponent(LayerComponent(i_theme, i_world, name)) for name in i_world.layerNames
        ]

        self.__font = i_theme.getFont("default")
        self.__brushLayer = "ground"

    def processInput(self):
        pass

    def update(self):
        self.__logic.executeCommands()

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

    
    def __computeCellCoordinates(self, i_pixel: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convert the mouse coordinates from pixels to cells.
        """
        tile_size = self.theme.getTileset(self.__brushLayer).tileSize
        # Use vectorDivI to divide pixel coordinates by tile size
        coords = vectorDivI(i_pixel, tile_size)

        # If out of render window
        if not self.__world.contains(coords):
            return None

        return coords

    def __updateCell(self, cell: Tuple[int, int], i_mouse : Mouse):
        
        layer = self.__world.getLayer(self.__brushLayer)
        # update cell based on mouse button (left or right)
        if i_mouse.button1 or i_mouse.button2:
            if self.__brushLayer == "ground":
                # If layer is ground, set value to ground
                value = CellValue.GROUND_EARTH
            
            elif self.__brushLayer != "ground":
                # Else, choose random value
                minValue = CellValueRanges[self.__brushLayer][0]
                maxValue = CellValueRanges[self.__brushLayer][1]
                value = CellValue(random.randint(minValue, maxValue - 1))  

            # Set fill to True if middle mouse button is pressed
            fill = i_mouse.button2  

        elif i_mouse.button3:
            # "delete" appropriately
            if self.__brushLayer == "ground":
                value = CellValue.GROUND_SEA
            
            else:
                value = CellValue.NONE
            fill = False
        else:
            return
        
        # Get the appropriate set layer value command and add it to waiting commands.
        Command = self.__logic.getSetLayerValueCommand(self.__brushLayer)
        command = Command(cell, value, fill)
        self.__logic.addCommand(command)
        


    def mouseButtonDown(self, i_mouse : Mouse):
        cellCoordinates = self.__computeCellCoordinates(i_mouse.coords)

        # If none, means we are outside render window
        if cellCoordinates is None:
            return

        self.__mouseButtonDown = True
        self.__updateCell(cellCoordinates, i_mouse)

    def mouseMove(self, i_mouse : Mouse):
        if not self.__mouseButtonDown:
            return

        cellCoordinates = self.__computeCellCoordinates(i_mouse.coords)

        if cellCoordinates is None:
            return

        self.__updateCell(cellCoordinates, i_mouse)
    
    def mouseButtonUp(self, i_mouse : Mouse):
        self.__mouseButtonDown = False

    def mouseEnter(self, i_mouse : Mouse):
        self.__mouseButtonDown = False

    def mouseLeave(self):
        self.__mouseButtonDown = False
