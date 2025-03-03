
from typing import Optional, Union

from core.state import World
from ui.Mouse import Mouse
from ui.theme.Theme import Theme
from ui.component.control.Button import Button
from .FrameComponent import FrameComponent

class PaletteFrame(FrameComponent):
    """A frame that displays buttons for selecting tiles."""
    
    def __init__(self, i_theme: Theme, i_world: World, i_rowCount: int = 2):
        super().__init__(i_theme)
        
        # Create buttons for each layer and tile
        prev_button: Optional[Button] = None
        for name in i_world.layerNames:
            prev_button = self.__addTilesetButtons(name, i_rowCount, prev_button)
            
        # Pack the frame to fit all buttons
        self.pack()
        
    def __createButton(self, i_layerName: str, i_tileId: Union[str, int]) -> Button:
        """Create a button for a specific tile."""
        def buttonAction(i_mouse: Mouse):
            """Action to perform when the button is clicked."""
            if i_mouse.button1:
                self.notifyMainBrushSelected(i_layerName, i_tileId)
            elif i_mouse.button3:
                self.notifySecondaryBrushSelected(i_layerName, i_tileId)
                
        # Get the tile surface from the tileset
        tileset = self.theme.getTileset(i_layerName)
        tile = tileset.getTile(i_tileId)
        
        # Create and return the button
        return Button(self.theme, tile, buttonAction)
        
    def __addTilesetButtons(self, i_layerName: str, i_rowCount: int,
                            i_columnButton: Optional[Button] = None) -> Optional[Button]:
        """Add buttons for each tile in the tileset."""
        tileset = self.theme.getTileset(i_layerName)
        previousButton: Optional[Button] = None
        columnIndex = 0
        
        # Iterate through each tile ID in the tileset
        for tileId in tileset.getTilesId():
            button = self.__createButton(i_layerName, tileId)
            
            # Position the button relative to the frame or previous buttons
            if i_columnButton is None:
                i_columnButton = button
                button.moveRelativeTo("topLeft", self, "topLeft", i_borderSize=0)
            elif columnIndex == 0:
                button.moveRelativeTo("left", i_columnButton, "right", i_borderSize=0)
            else:
                button.moveRelativeTo("top", previousButton, "bottom", i_borderSize=0)
            
            # Add the button to the frame
            self.addComponent(button)
            previousButton = button
            
            # Update column button and index
            if columnIndex == 0:
                i_columnButton = button
            columnIndex += 1
            if columnIndex >= i_rowCount:
                columnIndex = 0

        return i_columnButton