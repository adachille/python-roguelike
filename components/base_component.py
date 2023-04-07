"""File defining the basic functionality of any component."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    """Class defining the basic functionality of any component."""

    entity: Entity  # Owning entity instance.

    @property
    def engine(self) -> Engine:
        """Engine owning the entity this component is attached to."""
        return self.entity.gamemap.engine
