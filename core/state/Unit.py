import copy

from core.constants import UnitClass, UnitProperties, UnitProperty


class Unit:
    """Represents a game unit with properties and player ownership"""

    def __init__(self, unitClass: UnitClass, playerId: int = 0):
        self.__playerId = playerId
        self.__unitClass = unitClass
        if unitClass not in UnitProperties:
            raise ValueError(f"Invalid class {unitClass}")
        self.__properties = copy.deepcopy(UnitProperties[unitClass])

    @property
    def playerId(self) -> int:
        return self.__playerId

    @playerId.setter
    def playerId(self, playerId: int):
        self.__playerId = playerId

    @property
    def unitClass(self) -> UnitClass:
        return self.__unitClass

    def hasProperty(self, property: UnitProperty) -> bool:
        return property in self.__properties

    def setProperty(self, property: UnitProperty, value: int):
        self.__properties[property] = value

    def getProperty(self, property: UnitProperty) -> int:
        return self.__properties[property]
