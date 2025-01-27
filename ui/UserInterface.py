import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
from state.World import World
from state.constants import LAYER_GROUND_EARTH, LAYER_GROUND_SEA


class UserInterface:
    def __init__(self, input_world : World):
        self.__world = input_world

        pygame.init()
        # Create a resizable window of size 1920 x 1080, with faster rendering on screen
        self.__window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        # Set game caption and icon
        pygame.display.set_caption("TacticsGame")
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

        # Load tileset, define tile size, and define location of tiles in tileset
        self.__tileset = pygame.image.load("assets/toen/ground.png")
        self.__tileWidth = 16
        self.__tileHeight = 16
        self.__tiles = {
            LAYER_GROUND_EARTH: (2, 7),
            LAYER_GROUND_SEA: (5, 7),
        }
        self.__clock = pygame.time.Clock()


