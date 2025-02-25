"""
The Theme class. Contains all data related to the user-interface,
like the size of tiles or the used tilesets.
"""

import os
from typing import Dict, Tuple, Union, Optional

import pygame
from pygame.font import Font
from pygame.surface import Surface

from core.constants import CellValue
from .Tileset import Tileset


class Theme:
    def __init__(self):
        # Initialize caches for image surfaces and tilesets.
        self.__surfaces: Dict[str, Surface] = {}
        self.__tilesets: Dict[str, Tileset] = {}

        # Build tilesets from the definitions in tilesDefs.
        for name, tilesDef in tilesDefs.items():
            # Create a Tileset with the specified tile size and image file.
            tileset = Tileset(self, tilesDef["tileSize"], tilesDef["imageFile"])

            # Add each tile (value and its coordinates) to the tileset.
            for value, coords in tilesDef["tiles"].items():
                tileset.addTile(value, coords)

            # Store the constructed tileset using its name as the key.
            self.__tilesets[name] = tileset

        # Define default font settings.
        self.__fontsDef = {
            "default": {
                "file": "font/prstart/prstartk.ttf",
                "size": 8
            }
        }
        # Define default font colors.
        self.__fontColors = {
            "default": (100, 75, 50)
        }
        # Initialize a cache for loaded font objects.
        self.__fonts = {}

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


# Tile definitions for various layers (e.g., ground, impassable, objects).
tilesDefs = {
    "ground": {
        "imageFile": "toen/ground.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.GROUND_SEA: (4, 7),
            CellValue.GROUND_EARTH: (2, 7),
        }
    },
    "impassable": {
        "imageFile": "toen/impassable.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.IMPASSABLE_RIVER: (0, 1),
            CellValue.IMPASSABLE_POND: (1, 0),
            CellValue.IMPASSABLE_MOUNTAIN: (4, 0),
        }
    },
    "objects": {
        "imageFile": "toen/objects.png",
        "tileSize": (16, 16),
        "tiles": {
            CellValue.OBJECTS_SIGN: (1, 0),
            CellValue.OBJECTS_HILL: (4, 0),
            CellValue.OBJECTS_ROCKS: (6, 1),
            CellValue.OBJECTS_TREES: (5, 0),
            CellValue.OBJECTS_MILL: (0, 1),
            CellValue.OBJECTS_HOUSES: (1, 2),
            CellValue.OBJECTS_ROAD_DIRT: (0, 3),
            CellValue.OBJECTS_ROAD_STONE: (4, 3),
            CellValue.OBJECTS_FARM: (8, 0),
            CellValue.OBJECTS_CAMP: (8, 1),
        },
    },
}