"""Functionality for rendering."""
from __future__ import annotations

from typing import TYPE_CHECKING, List

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> List[str]:
    """Return names of entities at location."""
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return []

    return [
        entity.name.capitalize()
        for entity in game_map.entities
        if entity.x == x and entity.y == y
    ]


def render_status_bar(
    console: Console,
    status_type: str,
    current_value: int,
    maximum_value: int,
    width: int,
    y: int,
) -> None:
    """Render a status bar."""
    bar_width = int(float(current_value) / maximum_value * width)

    console.draw_rect(x=0, y=y, width=width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=y, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1,
        y=y,
        string=f"{status_type}: {current_value}/{maximum_value}",
        fg=color.bar_text,
    )


def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    """Render names of entities at a mouse location."""
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    # print(names_at_mouse_location, mouse_x, mouse_y)
    if not names_at_mouse_location:
        return

    console.print(x=x, y=y, string=", ".join(names_at_mouse_location))
