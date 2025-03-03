from typing import Optional, Tuple, List

import pygame
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from tools.vector import vectorDivF
from ui.IUIEventHandler import IUIEventHandler
from ui.Mouse import Mouse
from ui.MouseWheel import MouseWheel
from ui.component.Component import Component  # Added Component import
from ui.mode.GameMode import GameMode
from ui.theme.Theme import Theme

class UserInterface:
    """Main user interface class that handles rendering and input"""
    
    def __init__(self, theme: Theme):
        # Initialize pygame
        pygame.init()
        self.__window = pygame.display.set_mode((1024, 768), HWSURFACE | DOUBLEBUF | RESIZABLE)
        pygame.display.set_caption("TacticsGame")
        pygame.display.set_icon(pygame.image.load("assets/toen/icon.png"))
        
        # Rendering properties
        self.__theme = theme
        self.__rescaledShift = (0, 0)
        self.__rescaledScale = (1.0, 1.0)
        self.__renderSize = (self.__window.get_width(), self.__window.get_height())
        self.__font = theme.getFont("default")
        
        # Input handling - changed from boolean to Component
        self.__mouseFocus: Optional[Component] = None
        
        # Game properties
        self.__gameMode: Optional[GameMode] = None
        self.__running = True
        self.__clock = pygame.time.Clock()
    
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    def setGameMode(self, gameMode: GameMode):
        """Set the current game mode"""
        self.__gameMode = gameMode
    
    def setRenderSize(self, width: int, height: int):
        """Set the render size"""
        self.__renderSize = (width, height)
    
    def getEventHandlers(self) -> List[IUIEventHandler]:
        """Get all event handlers"""
        return [mode for mode in [
            self.__gameMode
        ] if mode is not None]
    
    # New method to find which component should have mouse focus
    def findMouseFocus(self, mouse: Mouse) -> Optional[Component]:
        """Find component that should receive mouse focus"""
        for handler in self.getEventHandlers():
            focus = handler.findMouseFocus(mouse)
            if focus is not None:
                return focus
        return None
    
    # Event handling methods
    def handleKeyDown(self, key: int) -> bool:
        """Handle key press event"""
        for handler in self.getEventHandlers():
            if handler.keyDown(key):
                return True
        return False
    
    def handleKeyUp(self, key: int) -> bool:
        """Handle key release event"""
        for handler in self.getEventHandlers():
            if handler.keyUp(key):
                return True
        return False
    
    def handleMouseEnter(self, mouse: Mouse) -> bool:
        """Handle mouse enter event"""
        for handler in self.getEventHandlers():
            if handler.mouseEnter(mouse):
                return True
        return False
    
    def handleMouseLeave(self) -> bool:
        """Handle mouse leave event"""
        for handler in self.getEventHandlers():
            if handler.mouseLeave():
                return True
        return False
    
    def handleMouseButtonDown(self, mouse: Mouse) -> bool:
        """Handle mouse button press event"""
        for handler in self.getEventHandlers():
            if handler.mouseButtonDown(mouse):
                return True
        return False
    
    def handleMouseButtonUp(self, mouse: Mouse) -> bool:
        """Handle mouse button release event"""
        for handler in self.getEventHandlers():
            if handler.mouseButtonUp(mouse):
                return True
        return False
    
    def handleMouseWheel(self, mouse: Mouse, wheel: MouseWheel) -> bool:
        """Handle mouse wheel event"""
        for handler in self.getEventHandlers():
            if handler.mouseWheel(mouse, wheel):
                return True
        return False
    
    def handleMouseMove(self, mouse: Mouse) -> bool:
        """Handle mouse movement event"""
        for handler in self.getEventHandlers():
            if handler.mouseMove(mouse):
                return True
        return False
    
    def __createMouse(self) -> Mouse:
        """Create a Mouse object from current mouse position"""
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX = int((mouseX - self.__rescaledShift[0]) / self.__rescaledScale[0])
        mouseY = int((mouseY - self.__rescaledShift[1]) / self.__rescaledScale[1])
        pygameButtons = pygame.mouse.get_pressed(num_buttons=3)
        return Mouse((mouseX, mouseY), pygameButtons)
    
    def __updateMouseFocus(self):
        """Update which component has mouse focus"""
        if pygame.mouse.get_focused():
            mouse = self.__createMouse()
            newFocus = self.findMouseFocus(mouse)
        else:
            mouse = Mouse((-10000, -10000))
            newFocus = None
            
        if newFocus != self.__mouseFocus:
            if self.__mouseFocus is not None and isinstance(self.__mouseFocus, IUIEventHandler):
                self.__mouseFocus.mouseLeave()
            self.__mouseFocus = newFocus
            if self.__mouseFocus is not None and isinstance(self.__mouseFocus, IUIEventHandler):
                self.__mouseFocus.mouseEnter(mouse)
    
    def __processKeyEvent(self, event):
        """Process keyboard events"""
        if event.type == pygame.KEYDOWN:
            self.handleKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            self.handleKeyUp(event.key)
    
    def __processMouseEvent(self, event):
        """Process mouse events"""
        mouse = self.__createMouse()
        viewSize = self.__theme.viewSize
        
        if 0 <= mouse.coords[0] < viewSize[0] and 0 <= mouse.coords[1] < viewSize[1]:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handleMouseButtonDown(mouse)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handleMouseButtonUp(mouse)
            elif event.type == pygame.MOUSEWHEEL:
                wheel = MouseWheel(event.x, event.y, event.flipped)
                self.handleMouseWheel(mouse, wheel)
            elif event.type == pygame.MOUSEMOTION:
                self.handleMouseMove(mouse)
    
    def processInput(self):
        """Process all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
                break
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                    break
                self.__processKeyEvent(event)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, 
                               pygame.MOUSEWHEEL, pygame.MOUSEMOTION):
                self.__processMouseEvent(event)
        
        # Update mouse focus after processing all events
        self.__updateMouseFocus()
    
    def update(self):
        """Update game state"""
        if self.__gameMode is not None:
            self.__gameMode.update()
    
    def render(self):
        """Render the game"""
        # Render to a surface
        renderSurface = Surface(self.__theme.viewSize)
        if self.__gameMode is not None:
            self.__gameMode.render(renderSurface)
        
        # Scale the rendered surface to fit the window
        windowWidth, windowHeight = self.__window.get_size()
        viewSize = self.__theme.viewSize
        renderRatio = viewSize[0] / viewSize[1]
        windowRatio = windowWidth / windowHeight
        
        if windowRatio <= renderRatio:
            rescaledSize = (windowWidth, int(windowWidth / renderRatio))
            self.__rescaledShift = (0, (windowHeight - rescaledSize[1]) // 2)
        else:
            rescaledSize = (int(windowHeight * renderRatio), windowHeight)
            self.__rescaledShift = ((windowWidth - rescaledSize[0]) // 2, 0)
        
        # Scale and blit the rendered surface
        rescaledSurface = pygame.transform.scale(renderSurface, rescaledSize)
        self.__rescaledScale = vectorDivF(rescaledSurface.get_size(), renderSurface.get_size())
        self.__window.blit(rescaledSurface, self.__rescaledShift)
        
        # Draw frame time
        frameTime = self.__clock.get_rawtime()
        textSurface = self.__font.render(f"{frameTime}ms", False, (255, 255, 255), (0, 0, 0))
        self.__window.blit(
            textSurface, (
                self.__window.get_width() - textSurface.get_width(),
                self.__window.get_height() - textSurface.get_height()
            )
        )
    
    def run(self):
        """Run the game loop"""
        while self.__running:
            self.processInput()
            self.update()
            self.render()
            
            pygame.display.update()
            self.__clock.tick(30)
        
        if self.__gameMode is not None:
            self.__gameMode.dispose()
    
    def quit(self):
        """Quit the game"""
        pygame.quit()
