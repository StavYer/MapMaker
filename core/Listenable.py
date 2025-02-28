# core/Listenable.py
from __future__ import annotations

import logging
from typing import List, TypeVar, Generic, Iterable

IListener = TypeVar('IListener')

class Listenable(Generic[IListener]):
    """Base class for objects that can be observed by listeners."""

    def __init__(self):
        self.__listeners: List[IListener] = []

    @property
    def listeners(self) -> Iterable[IListener]:
        """Get all registered listeners."""
        return self.__listeners

    def registerListener(self, listener: IListener):
        """Register a listener to receive notifications."""
        self.__listeners.append(listener)

    def removeListener(self, listener: IListener):
        """Remove a listener to stop receiving notifications."""
        self.__listeners.remove(listener)

    def removeAllListeners(self):
        """Remove all listeners."""
        self.__listeners.clear()

    def __del__(self):
        """Warn about listeners that were not removed when object is destroyed."""
        for listener in self.__listeners:
            logging.warning(f"In {self.__class__.__name__}: a listener {listener.__class__.__name__} was not removed")