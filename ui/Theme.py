from typing import Dict, Tuple

import pygame
from pygame import Surface

from state.constants import LAYER_GROUND_EARTH, LAYER_GROUND_SEA


class Theme:
    def __init__(self):
        # Load tileset, define tile size, and define location of tiles in tileset
        self.__tileset = pygame.image.load("assets/toen/ground.png")
        self.__tileWidth = 16
        self.__tileHeight = 16
        self.__tiles = {
            LAYER_GROUND_EARTH: (2, 7),
            LAYER_GROUND_SEA: (5, 7),
        }

    # Getters and setters
    @property
    def tileWidth(self) -> int:
        return self.__tileWidth

    @property
    def tileHeight(self) -> int:
        return self.__tileHeight

    @property
    def tileset(self) -> Surface:
        return self.__tileset

    @property
    def tiles(self) -> Dict[int, Tuple[int, int]]:
        return self.__tiles