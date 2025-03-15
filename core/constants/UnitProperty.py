from __future__ import annotations
from enum import IntEnum


class UnitProperty(IntEnum):
    HIT_POINTS = 1
    MAX_HIT_POINTS = 2
    ACTION_POINTS = 3
    MAX_ACTION_POINTS = 4
    MELEE_ATTACK = 5
    MELEE_DEFENSE = 6
    RANGE_ATTACK = 7
    RANGE_DEFENSE = 8
    MOUNT_ATTACK = 9
    MOUNT_DEFENSE = 10
    SIEGE_ATTACK = 11
    SIEGE_DEFENSE = 12
    BUILDING_ATTACK = 13
    BUILDING_DEFENSE = 14
