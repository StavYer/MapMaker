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
        # Call the parent class render method
        super().render(i_surface)
        
        # Get tileset surface and tile rectangles
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()
        tileWidth, tileHeight = self.tileset.tileSize
        
        # Loop through each cell in the layer
        for y in range(self.layer.height):
            for x in range(self.layer.width):
                value = self.layer[x, y]
                if value == CellValue.NONE:
                    continue
                    
                tile = (x * tileWidth, y * tileHeight)
                
                if self.autoTiling:
                    if value in [CellValue.OBJECTS_ROAD_DIRT, CellValue.OBJECTS_ROAD_STONE]:
                        # Check for bridge case (road over river)
                        impassableValue = self.__impassableLayer.getValue((x, y))
                        if impassableValue == CellValue.IMPASSABLE_RIVER:
                            # Check if the river is horizontal
                            left = self.__impassableLayer.getValue((x - 1, y))
                            right = self.__impassableLayer.getValue((x + 1, y))
                            riverHorizontal = (left == CellValue.IMPASSABLE_RIVER) and (right == CellValue.IMPASSABLE_RIVER)
                            
                            # Select appropriate bridge tile
                            if value == CellValue.OBJECTS_ROAD_DIRT:
                                rect = self.__bridgeDirtRects[riverHorizontal]
                            else:
                                rect = self.__bridgeStoneRects[riverHorizontal]
                        else:
                            # Normal road connections
                            neighbors = self.layer.getNeighbors4((x, y))
                            # Connect both dirt and stone roads
                            mask = mask4(neighbors, CellValue.OBJECTS_ROAD_DIRT)
                            mask = combine4(mask, mask4(neighbors, CellValue.OBJECTS_ROAD_STONE))
                            code = code4(mask)
                            
                            # Use appropriate road tileset
                            if value == CellValue.OBJECTS_ROAD_DIRT:
                                rect = self.__roadDirt_code2rect[code]
                            else:
                                rect = self.__roadStone_code2rect[code]
                    else:
                        # Regular objects with random variations
                        rects = tilesRects[value]
                        tileCount = len(rects)
                        rectIndex = self.noise[y][x] % tileCount
                        rect = rects[rectIndex]
                    
                    # Draw the selected tile
                    i_surface.blit(tileset, tile, rect)
                else:
                    # Simple rendering when auto-tiling is disabled
                    rect = tilesRects[value][0]
                    i_surface.blit(tileset, tile, rect)

