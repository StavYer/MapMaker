from .World import World


class GameState:
    def __init__(self, world: World):
        self.__currentPlayerId = 1
        self.__world = world

    @property
    def world(self) -> World:
        return self.__world

    @property
    def currentPlayerId(self) -> int:
        return self.__currentPlayerId
