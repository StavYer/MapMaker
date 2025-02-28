from typing import Optional

import pygame
from pygame import Rect
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from ui.Mouse import Mouse
from ui.MouseWheel import MouseWheel
from ui.Theme import Theme
from ui.mode import GameMode
from tools.vector import vectorDivF


class UserInterface:
    def __init__(self, input_theme : Theme):
        # Create a resizable window of size 1920 x 1080, with faster rendering on screen
        pygame.init()
        self.__window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        # Set game caption and icon
        pygame.display.set_caption("TacticsGame")
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))

        # Rendering
        self.__theme = input_theme
        self.__rescaledX = 0    # Horizontal offset of the rescaled game within the window.
        self.__rescaledY = 0    # Vertical offset of the rescaled game within the window.
        self.__rescaledScaleX = 1.0    # Horizontal scaling factor applied to the rendered surface.
        self.__rescaledScaleY = 1.0    # Vertical scaling factor applied to the rendered surface.
        self.__renderWidth = self.__window.get_width()
        self.__renderHeight = self.__window.get_height()

        # Inputs
        self.__mouseFocus = False

        # Other
        self.__gameMode : Optional[GameMode] = None
        self.__running = True
        self.__clock = pygame.time.Clock() 

    @property
    def theme(self) -> Theme:
        return self.__theme

    def setGameMode(self, i_gameMode: GameMode):
        self.__gameMode = i_gameMode

    def setRenderSize(self, i_renderWidth: int, i_renderHeight: int):
        self.__renderWidth = i_renderWidth
        self.__renderHeight = i_renderHeight
    
    def __processKeyEvent(self, i_event):
        # Check there is a game mode, otherwise there's no event to notify
        if self.__gameMode is None:
            return

        # If key is pressed, notify game mode
        if i_event.type == pygame.KEYDOWN:
            self.__gameMode.keyDown(i_event.key)

        # If key is released, notify game mode
        elif i_event.type == pygame.KEYUP:
            self.__gameMode.keyUp(i_event.key)
    
    def __processMouseEvent(self, i_event):
        # Check there is a game mode, otherwise there's no event to notify
        if self.__gameMode is None:
            return

        # If mouse leaves window, set focus to false and notify game mode
        if i_event.type == pygame.ACTIVEEVENT:
            if self.__mouseFocus:
                self.__mouseFocus = False
                self.__gameMode.mouseLeave()
            return

        # Build mouse data
        mouseX, mouseY = pygame.mouse.get_pos()  # Get mouse position in screen coordinates.
        mouseX = int((mouseX - self.__rescaledX) / self.__rescaledScaleX)  # Convert screen X to game world X.
        mouseY = int((mouseY - self.__rescaledY) / self.__rescaledScaleY)  # Convert screen Y to game world Y.
        # Get state of mouse buttons and store it
        pygameButtons = pygame.mouse.get_pressed(num_buttons=3)
        mouse = Mouse((mouseX, mouseY), pygameButtons)

        # If mouse is within the render window, notify the game mode appropriately
        if 0 <= mouseX < self.__renderWidth \
                and 0 <= mouseY < self.__renderHeight:  

            if not self.__mouseFocus:
                self.__mouseFocus = True
                self.__gameMode.mouseEnter(mouse)

            if i_event.type == pygame.MOUSEBUTTONDOWN:
                self.__gameMode.mouseButtonDown(mouse)

            elif i_event.type == pygame.MOUSEBUTTONUP:
                self.__gameMode.mouseButtonUp(mouse)

            elif i_event.type == pygame.MOUSEWHEEL:
                wheel = MouseWheel(i_event.x, i_event.y, i_event.flipped)
                self.__gameMode.mouseWheel(mouse, wheel)

            elif i_event.type == pygame.MOUSEMOTION:
                self.__gameMode.mouseMove(mouse)

        # Otherwise, notify that it's outside the render window.
        elif self.__mouseFocus:
            self.__mouseFocus = False
            self.__gameMode.mouseLeave()

    def processInput(self):
        """Handles all input events from the user."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:  # First, if user wants to quit
                    self.__running = False
                    break

                elif event.type == pygame.KEYDOWN \
                    or event.type == pygame.KEYUP:  # Else, handle keyboard events

                    # User wants to quit game
                    if event.key == pygame.K_ESCAPE:
                        self.__running = False
                        break
                    
                    self.__processKeyEvent(event)

                elif event.type == pygame.ACTIVEEVENT:
                    # Handle focus changes
                    if event.state & pygame.APPMOUSEFOCUS == pygame.APPMOUSEFOCUS:
                        # If the mouse focus state has changed, process mouse events
                        self.__processMouseEvent
                
                elif event.type == pygame.MOUSEBUTTONDOWN \
                        or event.type == pygame.MOUSEBUTTONUP \
                        or event.type == pygame.MOUSEMOTION \
                        or event.type == pygame.MOUSEWHEEL:
                         # Handle all mouse-related events (button presses, movement, wheel)
                    self.__processMouseEvent(event)

    def update(self):
        if self.__gameMode is not None:
            self.__gameMode.update()    

    def render(self):
        # Render world in a surface, and call GameMode's render method
        renderSurface = Surface((self.__renderWidth, self.__renderHeight))
        if self.__gameMode is not None:
            self.__gameMode.render(renderSurface)
        
        # Scale rendering when resizing window
            windowWidth, windowHeight = self.__window.get_size()
            renderRatio = self.__renderWidth / self.__renderHeight  # Compute aspect ratios of window and scene surfaces
            windowRatio = windowWidth / windowHeight

            if windowRatio <= renderRatio:  # We can use full window width but not height
                rescaledSurfaceWidth, rescaledSurfaceHeight = windowWidth, (windowWidth // renderRatio)
                self.__rescaledX = 0  # Compute coordinates of rescaled surface
                self.__rescaledY = (windowHeight - rescaledSurfaceHeight) // 2

            else:  # We can use full window height but not width
                rescaledSurfaceWidth, rescaledSurfaceHeight = int(windowHeight * renderRatio), windowHeight
                self.__rescaledX = (windowWidth - rescaledSurfaceWidth) // 2  # Compute coordinates again
                self.__rescaledY = 0
            
            # Scale the rendering to the window/screen size
            rescaledSurface = pygame.transform.scale(renderSurface, (rescaledSurfaceWidth, rescaledSurfaceHeight))
            # Calculate scale using vectorDivF
            scales = vectorDivF(rescaledSurface.get_size(), renderSurface.get_size())
            self.__rescaledScaleX = scales[0] 
            self.__rescaledScaleY = scales[1]
            self.__window.blit(rescaledSurface, (self.__rescaledX, self.__rescaledY))

    # main game loop
    def run(self):
        
        while self.__running:
            # Input handling
            self.processInput()
            # Update
            self.update()
            # Render
            self.render()

            pygame.display.update()
            self.__clock.tick(30)

    def quit(self):
        pygame.quit()
