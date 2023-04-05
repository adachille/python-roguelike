"""Holds action classes."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    """A class representing an action."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.
        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """A class for handling the escape action."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Exits game."""
        raise SystemExit()


class ActionWithDirection(Action):
    """A superclass for actions that have directionality."""

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """A class for handling the melee action."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform melee on entity."""
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack.

        print(f"You kick the {target.name}, much to its annoyance!")


class MovementAction(ActionWithDirection):
    """A class for handling the movement action."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform movement for an entity."""
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """A class handling the bump action."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Return an appropriate action depending on if there is a blocking entity."""
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
