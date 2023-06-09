"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
import input_handlers
from config import Config
from game_world import GameWorld

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("./bg-1.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    config = Config()
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)
    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=config.procgen["rooms"]["max_rooms"],
        room_min_size=config.procgen["rooms"]["min_size"],
        room_max_size=config.procgen["rooms"]["max_size"],
        map_width=config.view["map"]["width"],
        map_height=config.view["map"]["height"],
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        config.view["messages"]["welcome_message"], color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def __init__(self):
        super(MainMenu, self).__init__()
        self.config = Config()

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "Sun Bleach",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(self.config.view["menu"]["width"]),
                fg=color.menu_text,
                bg=color.menu_text_bg,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        """Handle user select."""
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
            pass
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
