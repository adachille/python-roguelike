"""Engine functionality."""
from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.context
from tcod.console import Console
from tcod.map import compute_fov

from config import Config
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_status_bar, render_names_at_mouse_location


if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler


class Engine:
    """Holds main game logic."""

    game_map: GameMap

    def __init__(self, player: Actor):
        self.config = Config()
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.context = None

    def handle_npc_turns(self) -> None:
        """Handle each NPC's turn."""
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def set_context(self, context: tcod.context.Context):
        """Set the context for the engine"""
        self.context = context

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=self.config.player["fov"]["radius"],
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        """Render entities on console."""
        self.game_map.render(console)

        # TODO: consider moving the render config directly into message log
        self.message_log.render(
            console=console,
            x=self.config.view["message_log"]["x"],
            y=self.config.view["message_log"]["y"],
            width=self.config.view["message_log"]["width"],
            height=self.config.view["message_log"]["height"],
        )

        # Render health bar
        render_status_bar(
            console=console,
            status_type="HP",
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            width=self.config.view["health_bar"]["width"],
            y=self.config.view["map"]["height"] + 2,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
