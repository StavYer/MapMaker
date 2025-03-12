from pygame import Rect, Surface

from .TextToken import TextToken


class IconTextToken(TextToken):

    def __init__(self, tileset: Surface, tile: Rect):
        self.__tileset = tileset
        self.__tile = tile

    @property
    def tileset(self) -> Surface:
        return self.__tileset

    @property
    def tile(self) -> Rect:
        return self.__tile