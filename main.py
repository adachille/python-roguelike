#!/usr/bin/env python3
import copy
import traceback

import tcod

import color
import entity_factories
from config import Config
from engine import Engine
from procgen import generate_dungeon


def main() -> None:
    config = Config()

    tileset = tcod.tileset.load_tilesheet(
        config.paths["tileset"], 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)
    engine.game_map = generate_dungeon(
        max_items_per_room=config.procgen["rooms"]["max_items_per_room"],
        max_monsters_per_room=config.procgen["rooms"]["max_monsters_per_room"],
        max_rooms=config.procgen["rooms"]["max_rooms"],
        room_min_size=config.procgen["rooms"]["min_size"],
        room_max_size=config.procgen["rooms"]["max_size"],
        map_width=config.view["map"]["width"],
        map_height=config.view["map"]["height"],
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        config.view["messages"]["welcome_message"], color.welcome_text
    )

    with tcod.context.new_terminal(
        config.view["screen"]["width"],
        config.view["screen"]["height"],
        tileset=tileset,
        title=config.view["title"],
        vsync=True,
    ) as context:
        engine.set_context(context)
        # Order "F" allows us to access tiles with (x,y) instead of (y,x)
        root_console = tcod.Console(
            config.view["screen"]["width"],
            config.view["screen"]["height"],
            order="F",
        )

        while True:
            root_console.clear()
            # TODO: can the below line not be replaced with `engine.render(console)`
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    event = context.convert_event(event)
                    engine.event_handler.handle_event(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
