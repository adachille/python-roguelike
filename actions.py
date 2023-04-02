"""Holds action classes."""


class Action:
    """A class representing an action."""

    pass


class EscapeAction(Action):
    """A class for handling the escape action."""

    pass


class MovementAction(Action):
    """A class for handling the movement action."""

    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy
