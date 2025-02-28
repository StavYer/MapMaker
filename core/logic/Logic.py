from abc import ABCMeta
from typing import Dict

from .Command import Command
from ..state import World

from .commands.SetGroundValueCommand import SetGroundValueCommand
from .commands.SetImpassableValueCommand import SetImpassableValueCommand
from .commands.SetObjectsValueCommand import SetObjectsValueCommand


class Logic:
    """Handles commands and logic for a world."""

    def __init__(self, i_world: World):
        self.__commands = {}  # type: Dict[int, Command]
        self.__world = i_world

    @property
    def world(self) -> World:
        return self.__world

    def addCommand(self, i_command: Command):
        self.__commands[i_command.priority()] = i_command

    def executeCommands(self):
        # Makes sure commands are added to the attribute before we execute them.
        commands = self.__commands.copy()
        self.__commands.clear()

        # Sort commands by priority and execute
        priorities = sorted(commands.keys())
        for priority in priorities:
            command = commands[priority]
            if not command.check(self):
                continue
            command.execute(self)

    def getSetLayerValueCommand(self, i_layer: str) -> ABCMeta:
        setLayerValueCommand = {
            "ground": SetGroundValueCommand,
            "impassable": SetImpassableValueCommand,
            "objects": SetObjectsValueCommand,
        }
        
        return setLayerValueCommand[i_layer]

