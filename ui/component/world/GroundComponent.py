from pygame import Surface

from core.constants import CellValue
from core.state import World
from tools.tilecodes import mask8, code8
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class GroundComponent(LayerComponent):
    def __init__(self, i_theme: Theme, i_world: World):
        # Initialize the GroundComponent with theme and world
        super().__init__(i_theme, i_world, "ground")
        self.__code2rect = self.tileset.getCode8Rects(0, 0)

    def render(self, i_surface: Surface):
        super().render(i_surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        # Get dimensions for rendering calculations
        tileWidth, tileHeight = self.tileset.tileSize
        layerWidth, layerHeight = self.layer.size
        surfaceWidth, surfaceHeight = i_surface.get_size()
        viewX, viewY = self.view
        
        # Iterate through visible tile positions
        for y in range(0, surfaceHeight + 1, tileHeight):
            cellY = (y + viewY) // tileHeight
            # Skip if cell is outside layer bounds
            if cellY < 0 or cellY >= layerHeight:
                continue
            for x in range(0, surfaceWidth + 1, tileWidth):
                cellX = (x + viewX) // tileWidth
                # Skip if cell is outside layer bounds
                if cellX < 0 or cellX >= layerWidth:
                    continue
                dest = (x - viewX % tileWidth, y - viewY % tileHeight)

                # Get cell value and skip empty cells
                value = self.layer.get_cell_value((cellX, cellY))
                if value == CellValue.NONE:
                    continue
                
                # Select tile variation using noise for visual diversity
                rects = tilesRects[value]
                tileCount = len(rects)
                rectIndex = self.noise[cellY][cellX] % tileCount
                i_surface.blit(tileset, dest, rects[rectIndex])
                
                # Handle sea tile edge transitions
                if value == CellValue.GROUND_SEA:
                    neighbors = self.layer.getNeighbors8((cellX, cellY))
                    mask = mask8(neighbors, CellValue.GROUND_SEA)
                    code = code8(mask)
                    rect = self.__code2rect[code]
                    i_surface.blit(tileset, dest, rect)
