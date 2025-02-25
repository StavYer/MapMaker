from enum import IntEnum

class CellValue(IntEnum):
    NONE = 0
    LAYER_GROUND_SEA = 101
    LAYER_GROUND_EARTH = 102

    IMPASSABLE_RIVER = 201
    IMPASSABLE_POND = 202
    IMPASSABLE_MOUNTAIN = 203

    OBJECTS_SIGN = 301
    OBJECTS_HILL = 302
    OBJECTS_ROCKS = 303
    OBJECTS_MILL = 305
    OBJECTS_HOUSES = 306
    OBJECTS_ROAD_DIRT = 307
    OBJECTS_ROAD_STONE = 308
    OBJECTS_CAMP = 309
    OBJECTS_FRAM = 310

CellValueRanges = {
    "ground": (101, 103),
    "impassable": (201, 204),
    "objects": (301, 311)
}
