"""Component that enable fighting for an entity."""
from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    """Component that enable fighting for an entity."""

    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        """The health points of owning entity."""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Set the health points of owning entity."""
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        """Returns overall defense."""
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        """Returns overall power."""
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        """Defense bonus afforded by equipment."""
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        """Power bonus afforded by equipment."""
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def heal(self, amount: int) -> int:
        """Heal health and return amount recovered."""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def take_damage(self, amount: int) -> None:
        """Take damage."""
        self.hp -= amount

    def die(self) -> None:
        """Makes the owning entity dead."""
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die
            self.engine.player.level.add_xp(self.parent.level.xp_given)

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"Remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
