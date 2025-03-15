from .UnitClass import UnitClass
from .UnitProperty import UnitProperty

UnitProperties = {
    UnitClass.WORKER: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
    },
    UnitClass.FARMER: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
    },
    UnitClass.BOWMAN: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
        UnitProperty.MELEE_ATTACK: 2,
        UnitProperty.MELEE_DEFENSE: 1,
        UnitProperty.RANGE_ATTACK: 2,
        UnitProperty.RANGE_DEFENSE: 1,
        UnitProperty.MOUNT_ATTACK: 2,
        UnitProperty.MOUNT_DEFENSE: 1,
        UnitProperty.SIEGE_ATTACK: 1,
        UnitProperty.SIEGE_DEFENSE: 1
    },
    UnitClass.PIKEMAN: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
        UnitProperty.MELEE_ATTACK: 2,
        UnitProperty.MELEE_DEFENSE: 2,
        UnitProperty.RANGE_ATTACK: 2,
        UnitProperty.RANGE_DEFENSE: 2,
        UnitProperty.MOUNT_ATTACK: 4,
        UnitProperty.MOUNT_DEFENSE: 4,
        UnitProperty.SIEGE_ATTACK: 2,
        UnitProperty.SIEGE_DEFENSE: 2,
        UnitProperty.BUILDING_ATTACK: 2
    },
    UnitClass.SWORDSMAN: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
        UnitProperty.MELEE_ATTACK: 3,
        UnitProperty.MELEE_DEFENSE: 3,
        UnitProperty.RANGE_ATTACK: 4,
        UnitProperty.RANGE_DEFENSE: 3,
        UnitProperty.MOUNT_ATTACK: 2,
        UnitProperty.MOUNT_DEFENSE: 3,
        UnitProperty.SIEGE_ATTACK: 2,
        UnitProperty.SIEGE_DEFENSE: 3,
        UnitProperty.BUILDING_ATTACK: 3
    },
    UnitClass.KNIGHT: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
        UnitProperty.MELEE_ATTACK: 3,
        UnitProperty.MELEE_DEFENSE: 2,
        UnitProperty.RANGE_ATTACK: 4,
        UnitProperty.RANGE_DEFENSE: 2,
        UnitProperty.MOUNT_ATTACK: 2,
        UnitProperty.MOUNT_DEFENSE: 2,
        UnitProperty.SIEGE_ATTACK: 4,
        UnitProperty.SIEGE_DEFENSE: 2,
        UnitProperty.BUILDING_ATTACK: 1
    },
    UnitClass.CATAPULT: {
        UnitProperty.HIT_POINTS: 0,
        UnitProperty.MAX_HIT_POINTS: 10,
        UnitProperty.ACTION_POINTS: 0,
        UnitProperty.MAX_ACTION_POINTS: 4,
        UnitProperty.MELEE_ATTACK: 1,
        UnitProperty.RANGE_ATTACK: 1,
        UnitProperty.MOUNT_ATTACK: 1,
        UnitProperty.SIEGE_ATTACK: 4,
        UnitProperty.BUILDING_ATTACK: 10
    }
}
