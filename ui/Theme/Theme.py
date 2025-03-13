"""
The Theme class. Contains all data related to the user-interface,
like the size of tiles or the used tilesets.
"""

import os
from typing import Dict, Tuple, Union, Optional

import pygame
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from core.constants import CellValue
from .Tileset import Tileset


class Theme:
    def __init__(self):
        self.__viewSize = (1024, 768)
        # Initialize caches for image surfaces and tilesets.
        self.__surfaces: Dict[str, Surface] = {}
        self.__tilesets: Dict[str, Tileset] = {}

        for name, tilesDef in tilesDefs.items():
            tileset = Tileset(self, tilesDef["tileSize"], tilesDef["imageFile"])
            tileset.addTiles(tilesDef["tiles"])
            self.__tilesets[name] = tileset

        # Set the frame border size based on the tile size of the "frame" tileset.
        self.__frameBorderSize = self.__tilesets["frame"].tileSize[0]

        self.__fontsDef = {
            "default": {
                "file": "font/prstart/prstartk.ttf",
                "size": 8,
                "crop": None
            },
            "small": {
                "file": "font/lilliputsteps/lilliputsteps.ttf",
                "size": 8,
                "crop": (3, 8)
            },
            "large": {
                "file": "font/prstart/prstartk.ttf",
                "size": 32,
                "crop": None
            },
        }
        self.__fontColors = {
            "default": Color(100, 75, 50),
            "warning": Color(200, 50, 35),
        }
        self.__fonts = {}

    @property
    def frameBorderSize(self) -> int:
        # Return the size of the frame border.
        return self.__frameBorderSize

    @property
    def viewSize(self) -> Tuple[int, int]:
        # Return the current view size.
        return self.__viewSize

    @viewSize.setter
    def viewSize(self, size: Tuple[int, int]):
        # Set the view size to the given value.
        self.__viewSize = size

    def getSurface(self, i_imageFile: str) -> Surface:
        # Return a cached Surface; load it if not already loaded.
        if i_imageFile not in self.__surfaces:
            fullPath = os.path.join("assets", i_imageFile)

            if not os.path.exists(fullPath):
                raise ValueError(f"No file '{fullPath}'")

            # Load the image and convert it for alpha transparency.
            self.__surfaces[i_imageFile] = pygame.image.load(fullPath).convert_alpha()

        return self.__surfaces[i_imageFile]

    def getTileset(self, i_name: str) -> Tileset:
        # Retrieve and return the Tileset by its name; error if not found.
        if i_name not in self.__tilesets:
            raise ValueError(f"No tileset {i_name}")

        return self.__tilesets[i_name]

    def getFont(self, i_name: Optional[str] = None) -> Font:
        # Return a Font object for the given name (default if None).
        if i_name is None:
            i_name = "default"

        if i_name not in self.__fontsDef:
            raise ValueError("No font {}".format(i_name))

        fontDef = self.__fontsDef[i_name]
        file = os.path.join("assets", fontDef["file"])
        size = fontDef["size"]
        fontId = (file, size)
        # Load and cache the font if it hasn't been loaded yet.
        if fontId not in self.__fonts:
            self.__fonts[fontId] = pygame.font.Font(file, size)

        return self.__fonts[fontId]

    def getFontColor(self, i_name: Union[None, str] = None) -> Tuple[int, int, int]:
        # Return the font color tuple for the given name (default if None).
        if i_name is None:
            i_name = "default"

        if i_name not in self.__fontColors:
            raise ValueError("No font color {}".format(i_name))
            
        return self.__fontColors[i_name]
    
    def getFontCrop(self, i_name: Optional[str] = None) -> Union[None, Tuple[int, int]]:
        if i_name is None:
            i_name = "default"
        if i_name not in self.__fontsDef:
            raise ValueError("No font {}".format(i_name))
        fontDef = self.__fontsDef[i_name]
        return fontDef["crop"]


# Tile definitions for various layers (e.g., ground, impassable, objects).
tilesDefs = {
    "ground": {
        "imageFile": "toen/ground.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.GROUND_SEA: [(4, 7), (5, 7), (6, 7), (7, 7)],
            CellValue.GROUND_EARTH: [(0, 7), (1, 7), (2, 7), (3, 7)],
        }
    },
    "impassable": {
        "imageFile": "toen/impassable.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.NONE: (0, 0),
            CellValue.IMPASSABLE_RIVER: (0, 1),
            CellValue.IMPASSABLE_POND: [(1, 0), (2, 0), (3, 0)],
            CellValue.IMPASSABLE_MOUNTAIN: [(4, 0), (5, 0), (6, 0)],
            "riverMouthRight": (4, 1),
            "riverMouthLeft": (4, 2),
            "riverMouthTop": (4, 3),
            "riverMouthBottom": (4, 4),
        }
    },
    "objects": {
        "imageFile": "toen/objects.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.NONE: (0, 0),
            CellValue.OBJECTS_SIGN: (1, 0),
            CellValue.OBJECTS_HILL: [(4, 0), (5, 1)],
            CellValue.OBJECTS_ROCKS: [(6, 1), (7, 1)],
            CellValue.OBJECTS_TREES: [(5, 0), (6, 0), (7, 0)],
            CellValue.OBJECTS_MILL: [(0, 1), (1, 1), (2, 1), (3, 1)],
            CellValue.OBJECTS_HOUSES: [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)],
            CellValue.OBJECTS_ROAD_DIRT: (0, 3),
            CellValue.OBJECTS_ROAD_STONE: (4, 3),
            CellValue.OBJECTS_FARM: [(8, 0), (9, 0), (10, 0), (11, 0)],
            CellValue.OBJECTS_CAMP: (8, 1),
            "bridgeDirt": [(0, 7), (1, 7)],
            "bridgeStone": [(4, 7), (5, 7)],
        },
    },
    "frame": {
        "imageFile": "toen/frame.png",
        "tileSize": (4, 4),
        "tiles": {
        "none": (0, 0),
        "arrowUp": (3, 1, 2, 2),
        "arrowDown": (5, 1, 2, 2),
        "arrowUpDisabled": (3, 3, 2, 2),
        "arrowDownDisabled": (5, 3, 2, 2),
        "topLeft": (0, 1),
        "top": (1, 1),
        "topRight": (2, 1),
        "left": (0, 2),
        "center": (1, 2),
        "right": (2, 2),
        "bottomLeft": (0, 3),
        "bottom": (1, 3),
        "bottomRight": (2, 3),
        "food": (7, 7, 2, 2),
        "gold": (9, 7, 2, 2),
        "wood": (11, 7, 2, 2),
        "stone": (13, 7, 2, 2),
        "dungeon": (17, 0, 8, 8),
    },
    },
    "icons": {
        "imageFile": "toen/icons.png",
        "tileSize": (5, 5),
        "tiles": {
        "food": (0, 0),
        "gold": (1, 0),
        "wood": (2, 0),
        "stone": (3, 0),
    },
    }
}

