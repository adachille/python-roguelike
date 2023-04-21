"""File defining the basic functionality of any component."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    """Class defining the basic functionality of any component."""

    parent: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        """Return gamemap."""
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        """Engine owning the entity this component is attached to."""
        return self.gamemap.engine
