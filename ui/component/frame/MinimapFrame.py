from typing import Optional, Tuple, cast

import numpy as np
import pygame
from pygame import Rect, Surface

from core.constants import CellValueRanges, CellValue
from core.state import World, ILayerListener, Layer
from tools.vector import vectorSubI, vectorMulI, vectorCenterI, vectorClampI
from .FrameComponent import FrameComponent
from ... import Mouse
from ...theme.Theme import Theme


class MinimapFrame(FrameComponent, ILayerListener):

    def __init__(self, i_theme: Theme, i_world: World):
        super().__init__(i_theme, (64, 48))
        self.__world = i_world
        self.__view = (0, 0)
        self.__minimapCoords = (0, 0)
        self.__tileSize = i_theme.getTileset("ground").tileSize
        self.__minimapSurface: Optional[Surface] = None

        # Initialize colors for each cell value range
        self.__colors = {}
        for name in ["ground", "impassable", "objects"]:
            tileset = i_theme.getTileset(name)
            valueRange = CellValueRanges[name]
            self.__colors[name] = tileset.getTilesColor(valueRange)


        # Register as a listener for each layer in the world
        for layer in self.__world.layers:
            layer.registerListener(self)

    def dispose(self):
        super().dispose()
        # Remove this object as a listener from each layer
        for layer in self.__world.layers:
            layer.removeListener(self)

    def __renderMinimap(self, cellsBox: Optional[Tuple[int, int, int, int]] = None):
        layers = zip(
            reversed(self.__world.layerNames),
            reversed(self.__world.layers)
        )
        if self.__minimapSurface is None or cellsBox is None:
            cellMinX, cellMaxX = 0, self.__world.width
            cellMinY, cellMaxY = 0, self.__world.height
        else:
            cellMinX, cellMaxX, cellMinY, cellMaxY = cellsBox
        cellsSlice = np.s_[cellMinX:cellMaxX, cellMinY:cellMaxY]
        minimapArray = np.zeros(
            [cellMaxX - cellMinX, cellMaxY - cellMinY, 4],
            dtype=np.int32
        )

        for name, layer in layers:
            cells = layer.cells[cellsSlice]
            if name == "units":
                playerColors = self.theme.playerColors
                validCells = cells == CellValue.UNITS_UNIT
                cellCoords = np.transpose(np.nonzero(validCells))
                for cell in cellCoords:
                    cellX = int(cellMinX + cell[0])
                    cellY = int(cellMinY + cell[1])
                    unit = layer.getUnit((cellX, cellY))
                    if unit is not None:
                        color = playerColors[unit.playerId]
                        minimapArray[cell[0], cell[1], :] = color
            else:
                colorMap = self.__colors[name]
                colors = colorMap[cells]
                transparent = minimapArray[..., 3] == 0
                minimapArray[transparent] = colors[transparent]

        minimapArea = pygame.surfarray.make_surface(minimapArray[..., 0:3]).convert()
        if self.__minimapSurface is None:
            self.__minimapSurface = minimapArea
        else:
            self.__minimapSurface.blit(minimapArea, (cellMinX, cellMinY))

    def render(self, i_surface: Surface):
        super().render(i_surface)

        # Compute the whole minimap if not already done
        if self.__minimapSurface is None:
            self.__renderMinimap()

        # Create a temporary surface to draw the minimap and rectangle
        innerArea = self.innerArea
        tempSurface = Surface(innerArea.size, flags=pygame.SRCALPHA)

        # Compute the location of the minimap and the view rectangle in the temporary surface
        def computeCoord(i_areaSize, i_worldSize, i_viewCoord, i_viewSize):
            if i_areaSize >= i_worldSize:  # Enough space to draw the whole map
                minimap = (i_areaSize - i_worldSize) // 2
                rect = minimap + i_viewCoord
            else:  # Not enough space
                rect = (i_areaSize - i_viewSize) // 2
                minimap = rect - i_viewCoord
                if minimap > 0:
                    rect -= minimap
                    minimap = 0
                minimapMin = i_areaSize - i_worldSize
                if minimap < minimapMin:
                    rect += minimapMin - minimap
                    minimap = minimapMin
            return minimap, rect

        tileWidth, tileHeight = self.__tileSize
        worldWidth, worldHeight = self.__world.size
        viewX = self.__view[0] // tileWidth
        viewY = self.__view[1] // tileHeight
        viewWidth = self.theme.viewSize[0] // tileWidth
        viewHeight = self.theme.viewSize[1] // tileHeight
        minimapX, rectX = computeCoord(innerArea.width, worldWidth, viewX, viewWidth)
        minimapY, rectY = computeCoord(innerArea.height, worldHeight, viewY, viewHeight)
        self.__minimapCoords = (minimapX, minimapY)

        # Draw minimap & view rectangle in the temporary surface
        if self.__minimapSurface is not None:
            tempSurface.blit(self.__minimapSurface, self.__minimapCoords)
        viewRect = Rect(rectX, rectY, viewWidth, viewHeight)
        pygame.draw.rect(tempSurface, (255, 255, 255), viewRect, width=1)

        # Draw the temporary surface (contains clipped minimap + view rectangle)
        i_surface.blit(tempSurface, innerArea.topleft)

    # UI Event handler

    def mouseButtonDown(self, i_mouse: Mouse) -> bool:
        if not i_mouse.button1:
            return True
        innerArea = self.innerArea
        if not innerArea.collidepoint(i_mouse.pixel):
            return True
        # Convert mouse pixel coordinates to pixel relative to minimap top left corner
        # Since one minimap pixel = cell, these coordinates are world cell coordinates
        cell = vectorSubI(i_mouse.pixel, innerArea.topleft)
        cell = vectorSubI(cell, self.__minimapCoords)
        if not self.__world.contains(cell):
            return True
        # Convert cell coordinates into pixel coordinates
        view = vectorMulI(cell, self.__tileSize)
        # Center so the cursor in the middle of the view
        view = vectorCenterI(view, self.theme.viewSize)
        worldSize = vectorMulI(self.__world.size, self.__tileSize)
        maxView = vectorSubI(worldSize, self.theme.viewSize)
        view = vectorClampI(view, 0, maxView)
        if view != self.__view:
            self.notifyViewChanged(view)
        return True

    def mouseMove(self, i_mouse: Mouse) -> bool:
        return self.mouseButtonDown(i_mouse)

    # Component listener

    def viewChanged(self, i_view: Tuple[int, int]):
        if i_view != self.__view:
            self.__view = i_view

    # Layer listener

    def cellChanged(self, i_layer: Layer, i_cell: Tuple[int, int]):
        cellX, cellY = i_cell
        cellMinX, cellMaxX = max(cellX, 0), min(cellX + 1, i_layer.width)
        cellMinY, cellMaxY = max(cellY, 0), min(cellY + 1, i_layer.height)
        self.__renderMinimap((cellMinX, cellMaxX, cellMinY, cellMaxY))
