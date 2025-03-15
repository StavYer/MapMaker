from enum import IntEnum
from typing import List

class CellValue(IntEnum):
    NONE = 0
    GROUND_SEA = 101
    GROUND_EARTH = 102

    IMPASSABLE_RIVER = 201
    IMPASSABLE_POND = 202
    IMPASSABLE_MOUNTAIN = 203

    OBJECTS_SIGN = 301
    OBJECTS_HILL = 302
    OBJECTS_ROCKS = 303
    OBJECTS_TREES = 304
    OBJECTS_MILL = 305
    OBJECTS_HOUSES = 306
    OBJECTS_ROAD_DIRT = 307
    OBJECTS_ROAD_STONE = 308
    OBJECTS_CAMP = 309
    OBJECTS_FARM = 310

    UNITS_UNIT = 401

    MAX_VALUE = 1000

CellValueRanges = {
    "ground": (101, 103),
    "impassable": (201, 204),
    "objects": (301, 311)
}

def getCellValues(i_layer: str) -> List[int]:
    values: List[int] = []
    if i_layer != "ground":
        values.append(CellValue.NONE)
    for value in range(*CellValueRanges[i_layer]):
        values.append(value)
    return values

def checkCellValue(layer: str, value: CellValue):
    """
    Checks if the given cell value is valid for the specified layer.
    """
    if layer != "ground" and value == CellValue.NONE:
        return True
    
    # check if whithin the range
    valueRange = CellValueRanges[layer]
    try:
        return valueRange[0] <= value < valueRange[1]
    except Exception as e:
        print(f"this is value: {value}")
        print(f"Error: {e}")
        
