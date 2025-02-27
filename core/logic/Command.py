from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .Logic import Logic

WORLD_PRIORITY = 100

WORLD_MAX_WIDTH = 4096
WORLD_MAX_HEIGHT = 4096


class Command(ABC):

    @abstractmethod
    def priority(self) -> int:
        """
        Returns the level of priority. Commands with a low priority value should run first.
        """
        raise NotImplementedError()

    @abstractmethod
    def check(self, logic: Logic) -> bool:
        """
        Returns True if the command is valid and does something.
        """
        raise NotImplementedError()

    @abstractmethod
    def execute(self, logic: Logic):
        """
        The actual processing. We assume that check() returned True and do the changes with no checks.
        """
        raise NotImplementedError()
