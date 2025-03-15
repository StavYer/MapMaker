from pygame.surface import Surface

from core.constants import CellValue
from core.state import World
from .LayerComponent import LayerComponent
from ...theme.Theme import Theme


class UnitsComponent(LayerComponent):
    """Component that renders units on the map"""
    
    def __init__(self, i_theme: Theme, i_world: World):
        """Initialize with theme and world reference"""
        super().__init__(i_theme, i_world, "units")
    
    def render(self, surface: Surface):
        """Render units to the surface"""
        super().render(surface)
        tileset = self.tileset.surface
        tilesRects = self.tileset.getTilesRects()

        renderer = self.createRenderer(surface)
        cellsSlice = renderer.cellsSlice
        cellMinX, _, cellMinY, _ = renderer.cellsBox
        cells = self.layer.cells[cellsSlice]

        valid = cells == CellValue.UNITS_UNIT
        for dest, value, cell in renderer.coords(valid):
            cellX, cellY = cellMinX + cell[0], cellMinY + cell[1]
            unit = self.layer.getUnit((cellX, cellY))
            if unit is not None:
                rects = tilesRects[unit.unitClass]
                surface.blit(tileset, dest, rects[unit.playerId])
