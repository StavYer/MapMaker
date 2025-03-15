
from typing import Optional, Union

from core.constants import UnitClass
from core.state import World, GameState
from pygame.surface import Surface
from core.constants.CellValue import getCellValues, CellValue
from ui.Mouse import Mouse
from ui.theme.Theme import Theme
from ui.component.control.Button import Button
from .FrameComponent import FrameComponent

class PaletteFrame(FrameComponent):
    """A frame that displays buttons for selecting tiles."""
    
    def __init__(self, i_theme: Theme, i_state: GameState, i_rowCount: int = 2):
        super().__init__(i_theme)
        
        self.__state = i_state
        self.__rowCount = i_rowCount
        self.__columnIndex = 0
        self.__columnButton: Optional[Button] = None
        self.__previousButton: Optional[Button] = None

        for layerName in ["ground", "impassable", "objects"]:
            self.__newColumn()
            tileset = self.theme.getTileset(layerName)
            for value in getCellValues(layerName):
                tile = tileset.getTile(value)
                self.__addButton(tile, layerName, value, None)

        self.__newColumn()
        tileset = self.theme.getTileset("units")
        for unitClass in UnitClass:
            tile = tileset.getTile(unitClass)
            if unitClass == UnitClass.NONE:
                self.__addButton(tile, "units", CellValue.NONE, None)
            else:
                self.__addButton(tile, "units", CellValue.UNITS_UNIT, unitClass)

        self.pack()
        
    def __addButton(self, tile: Surface, layerName: str, value: Union[str, int],
                    unitClass: Optional[UnitClass]):
        def buttonAction(mouse: Mouse):
            if mouse.button1:
                self.notifyMainBrushSelected(layerName, value, unitClass)
            elif mouse.button3:
                self.notifySecondaryBrushSelected(layerName, value, unitClass)

        button = Button(self.theme, tile, buttonAction)

        if self.__columnButton is None:
            self.__columnButton = button
            button.moveRelativeTo("topLeft", self, "topLeft", i_borderSize=0)
        elif self.__columnIndex == 0:
            button.moveRelativeTo("left", self.__columnButton, "right", i_borderSize=0)
        else:
            button.moveRelativeTo("top", self.__previousButton, "bottom", i_borderSize=0)
        self.addComponent(button)
        self.__previousButton = button
        if self.__columnIndex == 0:
            self.__columnButton = button
        self.__columnIndex += 1
        if self.__columnIndex >= self.__rowCount:
            self.__columnIndex = 0

    def __newColumn(self):
        self.__columnIndex = 0
        self.__previousButton = self.__columnButton