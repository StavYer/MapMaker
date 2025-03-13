import random
import pygame
from typing import Tuple, Union


from core.constants import CellValue, CellValueRanges
from core.state import World
from core.logic import Logic
from tools.vector import vectorMulI, vectorSubI, vectorClampI
from ..Mouse import Mouse
from ..theme.Theme import Theme
from .GameMode import GameMode
from ..component.frame.ResourcesFrame import ResourcesFrame
from ..component.IComponentListener import IComponentListener
from ..component.frame.MinimapFrame import MinimapFrame
from ..component.world.WorldComponent import WorldComponent
from ..component.frame.PaletteFrame import PaletteFrame


class EditGameMode(GameMode, IComponentListener):
    """Game mode for editing the world"""

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme)
        self.__world = i_world
        self.__logic = Logic(i_world)
        self.__font = i_theme.getFont("default")

        # Create world component
        self.__worldComponent = WorldComponent(i_theme, i_world)

        # Create resources frame
        self.__resourcesFrame = ResourcesFrame(i_theme)
        self.__resourcesFrame.moveRelativeTo("topLeft", self, "topLeft")
        
        # Create palette and minimap frame
        self.__paletteFrame = PaletteFrame(i_theme, i_world)
        self.__paletteFrame.moveRelativeTo("bottom", self, "bottom")

        self.__minimapFrame = MinimapFrame(i_theme, i_world)
        self.__minimapFrame.moveRelativeTo("bottomRight", self, "bottomRight")

        # Add components in order (world first, palette on top)
        self.addComponent(self.__worldComponent)
        self.addComponent(self.__resourcesFrame)
        self.addComponent(self.__paletteFrame)
        self.addComponent(self.__minimapFrame)

        # Set default brush values
        self.__mainBrushLayer = "ground"
        self.__mainBrushValue = CellValue.GROUND_EARTH
        self.__secondaryBrushLayer = "ground"
        self.__secondaryBrushValue :Union[int, str] = CellValue.GROUND_SEA

        # Register as listener
        self.__worldComponent.registerListener(self)
        self.__minimapFrame.registerListener(self)
        self.__paletteFrame.registerListener(self)

    def update(self):
        """Update game state"""
        self.__logic.executeCommands()

    def dispose(self):
        """Clean up resources"""
        self.__worldComponent.removeListener(self)
        self.__paletteFrame.removeListener(self)
        super().dispose()
        
    def keyDown(self, i_key: int) -> bool:
        """Handle key press event."""
        if i_key == pygame.K_F1:
            # Enable auto-tiling
            print("Auto-tiling enabled")
            self.__worldComponent.setAutoTiling(True)
            return True
        elif i_key == pygame.K_F2:
            # Disable auto-tiling
            print("Auto-tiling disabled")
            self.__worldComponent.setAutoTiling(False)
            return True
        return False

    # Component Listener methods
    def __updateCell(self, i_cell: Tuple[int, int], i_mouse: Mouse):
        """Update cell based on mouse input"""
        if i_mouse.button1 or i_mouse.button2:
            # Add cell value
            brushLayer = self.__mainBrushLayer
            brushValue = self.__mainBrushValue
            fill = i_mouse.button2
        elif i_mouse.button3:
            # Remove cell value
            brushLayer = self.__secondaryBrushLayer
            brushValue = self.__secondaryBrushValue
            fill = False
        else:
            return

        # Create and add command
        Command = self.__logic.getSetLayerValueCommand(brushLayer)
        command = Command(i_cell, brushValue, fill)
        self.__logic.addCommand(command)

    def worldCellClicked(self, i_cell: Tuple[int, int], i_mouse: Mouse):
        """Handle world cell click"""
        self.__updateCell(i_cell, i_mouse)

    def worldCellEntered(self, i_cell: Tuple[int, int], i_mouse: Mouse, i_dragging: bool):
        """Handle mouse entering a world cell"""
        if i_dragging:
            self.__updateCell(i_cell, i_mouse)
            
    def mainBrushSelected(self, i_layerName: str, i_value: Union[int, str]):
        """Called when the main brush is selected from palette"""
        self.__mainBrushLayer = i_layerName
        self.__mainBrushValue = i_value
        
    def secondaryBrushSelected(self, i_layerName: str, i_value: Union[int, str]):
        """Called when the secondary brush is selected from palette"""
        self.__secondaryBrushLayer = i_layerName
        self.__secondaryBrushValue = i_value

    def processInput(self) -> bool:
        """Process keyboard input for view movement"""
        # Update view using keyboard state
        keys = pygame.key.get_pressed()
        newViewX, newViewY = self.__worldComponent.view
        tileset = self.theme.getTileset("ground")
        tileWidth, tileHeight = tileset.tileSize
        if keys[pygame.K_RIGHT]:
            newViewX += tileWidth // 4
        if keys[pygame.K_LEFT]:
            newViewX -= tileWidth // 4
        if keys[pygame.K_UP]:
            newViewY -= tileHeight // 4
        if keys[pygame.K_DOWN]:
            newViewY += tileHeight // 4
        newView = (newViewX, newViewY)

        # Clamp new view
        worldSize = vectorMulI(self.__world.size, tileset.tileSize)
        maxView = vectorSubI(worldSize, self.theme.viewSize)
        newView = vectorClampI(newView, 0, maxView)

        # Update only if changes
        if newView != self.__worldComponent.view:
            self.viewChanged(newView)
            return True
        return False

  
