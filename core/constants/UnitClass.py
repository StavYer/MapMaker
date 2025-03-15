from __future__ import annotations

from enum import IntEnum


class UnitClass(IntEnum):
    NONE = 0
    WORKER = 1
    FARMER = 2
    BOWMAN = 3
    PIKEMAN = 4
    SWORDSMAN = 5
    KNIGHT = 6
    CATAPULT = 7

    @staticmethod
    def fromName(name: str) -> UnitClass:
        if name not in unitClassName2Id:
            raise ValueError(f"Invalid unit class name {name}")
        return unitClassName2Id[name]


unitClassId2Name = {
    UnitClass.WORKER: "Worker",
    UnitClass.FARMER: "Farmer",
    UnitClass.BOWMAN: "Bowman",
    UnitClass.PIKEMAN: "Pikeman",
    UnitClass.SWORDSMAN: "Swordsman",
    UnitClass.KNIGHT: "Knight",
    UnitClass.CATAPULT: "Catapult"
}

unitClassName2Id = {
    "Worker": UnitClass.WORKER,
    "Farmer": UnitClass.FARMER,
    "Bowman": UnitClass.BOWMAN,
    "Pikeman": UnitClass.PIKEMAN,
    "Swordsman": UnitClass.SWORDSMAN,
    "Knight": UnitClass.KNIGHT,
    "Catapult": UnitClass.CATAPULT
}