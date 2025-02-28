# core/state/ILayerListener.py
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .Layer import Layer


class ILayerListener:
    """Interface for objects that want to receive notifications about layer changes."""

    def cellChanged(self, i_layer: Layer, i_cell: Tuple[int, int]):
        """Called when a cell in a layer changes."""
        pass