"""Holds action classes."""
from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    """A class representing an action."""

    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """A class for handling the escape action."""

    def perform(self) -> None:
        """Exits game."""
        raise SystemExit()


class WaitAction(Action):
    """A class for handling the wait action."""

    def perform(self) -> None:
        """Do nothing for the turn."""
        pass


class ActionWithDirection(Action):
    """A superclass for actions that have directionality."""

    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this action's destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        """Perform action with direction, must be overridden by subclass."""
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """A class for handling the melee action."""

    def perform(self) -> None:
        """Perform melee on entity."""
        target = self.target_actor
        if not target:
            # TODO: this should probably return a warning, as it shouldn't happen
            return  # No entity to attack.

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            print(f"{attack_desc} for {damage} hit points.")
            target.fighter.hp -= damage
        else:
            print(f"{attack_desc} but does no damage.")


class MovementAction(ActionWithDirection):
    """A class for handling the movement action."""

    def perform(self) -> None:
        """Perform movement for an entity."""
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # TODO: this should probably return a warning, as it shouldn't happen
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """A class handling the bump action."""

    def perform(self) -> None:
        """Return an appropriate action depending on if there is a blocking entity."""
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
