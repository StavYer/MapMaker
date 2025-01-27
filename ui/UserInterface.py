import pygame
from pygame import Rect
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

    # main game loop
    def run(self):
        running = True
        while running:
            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # First, if user wants to quit
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:  # Else, if user pressed keyboard
                    # User wants to quit game
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
            # Rendering
            # Render world on a surface
            # Each tile in the world grid will be drawn as a rectangular image on the render surface.
            tileWidth, tileHeight = self.__tileWidth, self.__tileHeight # tile dimensions

            # compute render surface dimensions in pixels
            renderWidth = self.__world.width * tileWidth
            renderHeight = self.__world.height * tileHeight
            renderSurface = Surface((renderWidth, renderHeight))

            # loop through every part of the world grid
            for y in range(self.__world.height):
                for x in range(self.__world.width):
                    value = self.__world.get_cell_value(x, y)
                    tile = self.__tiles[value] # lookup tile coordinates in the tileset
                    # Define the rectangle (in the tileset) to extract the tile's graphic - portion to copy
                    tileRect = Rect(
                        tile[0] * tileWidth, tile[1] * tileHeight,
                        tileWidth, tileHeight
                    )
                    tileCoordinates = (x * tileWidth, y * tileHeight) # pos on render to draw this tile
                    renderSurface.blit(self.__tileset, tileCoordinates, tileRect) # draw tile onto render surface
            # Scale rendering when resizing window
            windowWidth, windowHeight = self.__window.get_size()
            renderRatio = renderWidth / renderHeight  # Compute aspect ratios of window and scene surfaces
            windowRatio = windowWidth / windowHeight

            if windowRatio <= renderRatio:  # We can use full window width but not height
                rescaledSurfaceWidth, rescaledSurfaceHeight = windowWidth, (windowWidth // renderRatio)
                rescaledSurfaceX = 0  # Compute coordinates of rescaled surface
                rescaledSurfaceY = (windowHeight - rescaledSurfaceHeight) // 2
            else:  # We can use full window height but not width
                rescaledSurfaceWidth, rescaledSurfaceHeight = int(windowHeight * renderRatio), windowHeight
                rescaledSurfaceX = (windowWidth - rescaledSurfaceWidth) // 2  # Compute coordinates again
                rescaledSurfaceY = 0

            # Scale the rendering to the window/screen size
            rescaledSurface = pygame.transform.scale(renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight))
            self.__window.blit(rescaledSurface, (rescaledSurfaceX, rescaledSurfaceY))
            pygame.display.update()

    def quit(self):
        pygame.quit()
