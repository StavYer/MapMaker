from pygame import Surface

from core.constants import CellValue
from core.state import World
from tools.tilecodes import mask4, combine4, code4
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class ObjectsComponent(LayerComponent):
    """Component that renders object features like roads, buildings"""
    
    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize with theme and world reference"""
        super().__init__(i_theme, i_world, "objects")
        # Get the impassable layer to check for rivers under bridges
        self.__impassableLayer = i_world.getLayer("impassable")
        # Get bridge tile rectangles
        self.__bridgeDirtRects = self.tileset.getTileRects("bridgeDirt")
        self.__bridgeStoneRects = self.tileset.getTileRects("bridgeStone")
        # Get lookup tables for road tiles
        self.__roadDirt_code2rect = self.tileset.getCode4Rects(0, 3)
        self.__roadStone_code2rect = self.tileset.getCode4Rects(4, 3)

    def render(self, i_surface: Surface):
        """Render objects with auto-tiling for roads and bridges"""
        super().render(i_surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()
        
        # Iterate over rendered cells
        for dest, value, cell in self.renderedCells(i_surface):
            if value == CellValue.NONE:
                continue
            
            # Handle road tiles
            if value in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:
                # Check for bridge over river
                impassableValue = self.__impassableLayer.get_cell_value(cell)
                if impassableValue == CellValue.IMPASSABLE_RIVER:
                    left = self.__impassableLayer.get_cell_value(cell, Direction.LEFT)
                    right = self.__impassableLayer.get_cell_value(cell, Direction.RIGHT)
                    riverHorizontal = (left == CellValue.IMPASSABLE_RIVER) and (right == CellValue.IMPASSABLE_RIVER)
                    if value == CellValue.OBJECTS_ROAD_DIRT:
                        rect = self.__bridgeDirtRects[riverHorizontal]
                    else:
                        rect = self.__bridgeStoneRects[riverHorizontal]
                else:
                    # Auto-tiling for roads
                    neighbors = self.layer.getNeighbors4(cell)
                    mask = mask4(neighbors, CellValue.OBJECTS_ROAD_DIRT)
                    mask = combine4(mask, mask4(neighbors, CellValue.OBJECTS_ROAD_STONE))
                    code = code4(mask)
                    rect = self.__roadDirt_code2rect[code]
            else:
                # Handle other object tiles
                rects = tilesRects[value]
                tileCount = len(rects)
                rectIndex = self.noise[cell[1]][cell[0]] % tileCount
                rect = rects[rectIndex]
            
            # Blit the tile to the surface
            i_surface.blit(tileset, dest, rect)