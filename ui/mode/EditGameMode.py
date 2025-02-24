from typing import Tuple, Optional

from pygame.rect import Rect
from pygame.surface import Surface

from state import World
from state.constants import LAYER_GROUND_EARTH, LAYER_GROUND_SEA
from ui.MouseButtons import MouseButtons
from ui.Theme import Theme
from ui.mode.GameMode import GameMode


class EditGameMode(GameMode):

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(theme)
        self.__world = i_world
        self.__mouseButtonDown = False # True if player clicked inside world

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self, i_surface: Surface):
        theme = self.theme\
        tileWidth = theme.tileWidth
        tileHeight = theme.tileHeight
        tiles = theme.tiles
        tileset = theme.tileset

        # loop through every part of the world grid
            for y in range(self.__world.height):
                for x in range(self.__world.width):
                    value = self.__world.get_cell_value(x, y)
                    tile = tiles[value] # lookup tile coordinates in the tileset
                    # Define the rectangle (in the tileset) to extract the tile's graphic - portion to copy
                    tileRect = Rect(
                        tile[0] * tileWidth, tile[1] * tileHeight,
                        tileWidth, tileHeight
                    )
                    tileCoordinates = (x * tileWidth, y * tileHeight) # pos on render to draw this tile
                    renderSurface.blit(self.__tileset, tileCoordinates, tileRect) # draw tile onto render surface

    # Mouse handling

    
    def __computeCellCoordinates(self, i_mouseX: int, i_mouseY: int) -> Optional[Tuple[int, int]]:
        """
        Convert the mouse coordinates from pixels to cells.
        """
        cellX = i_mouseX // self.theme.tileWidth
        cellY = i_mouseY // self.theme.tileHeight

        # If out of render window
        if not (0 <= cellX < self.__world.width) or not (0 <= cellY < self.__world.height):
            return None

        return cellX, cellY

    def __updateCell(self, i_cellX: int, i_cellY: int, buttons: MouseButtons):

        # update cell based on mouse button (left or right)
        if buttons.button1:
            self.__world.set_cell_value(i_cellX, i_cellY, LAYER_GROUND_EARTH)

        elif buttons.button3:
            self.__world.set_cell_value(i_cellX, i_cellY, LAYER_GROUND_SEA)

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
