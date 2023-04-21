"""Engine functionality."""
from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from config import Config
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    """Holds main game logic."""

    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.config = Config()
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)

    def handle_npc_turns(self) -> None:
        """Handle each NPC's turn."""
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.ActionCannotBePerformed:
                    pass  # Ignore failed action exceptions from AI.

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
        render_functions.render_status_bar(
            console=console,
            status_type="HP",
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            width=self.config.view["health_bar"]["width"],
            y=self.config.view["map"]["height"] + 2,
        )

        # Render dungeon level
        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(
                self.config.view["dungeon_level"]["x"],
                self.config.view["dungeon_level"]["y"],
            ),
        )

        # Render examine ui
        render_functions.render_names_at_mouse_location(
            console=console,
            x=self.config.view["examine_ui"]["x"],
            y=self.config.view["examine_ui"]["y"],
            engine=self,
        )
