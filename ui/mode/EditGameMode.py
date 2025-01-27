from pygame import Surface, Rect

from state import World
from ui import Theme
from ui.mode import GameMode


class EditGameMode(GameMode):
    def __init__(self, input_theme : Theme, input_world: World):
        super().__init__(input_theme)
        self.__world = input_world

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self, input_surface : Surface):
        theme = self.theme
        tileWidth, tileHeight = theme.tileWidth, theme.tileHeight
        tiles = theme.tiles
        tileset = theme.tileset

        # for each cell in the world, draw tile onto render surface
        for y in range(self.__world.height):
            for x in range(self.__world.width):
                tile = tiles[self.__world.get_cell_value(x, y)]
                tileRect = Rect(
                    tile[0] * tileWidth, tile[1] * tileHeight,
                    tileWidth, tileHeight
                )
                tileCoords = (
                    x * tileWidth,
                    y * tileHeight
                )
                input_surface.blit(tileset, tileCoords, tileRect)