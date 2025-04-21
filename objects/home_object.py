import asyncio
from typing import Callable

from objects.base_object import BaseObject
from typing import TYPE_CHECKING

from objects.player_object import PlayerObject
if TYPE_CHECKING:
    from screen.screen import Screen


class HomeObject(BaseObject):
    """
    Object which represents a player's base
    """
    def __init__(self, screen: 'Screen', x: int, y: int):
        self.symb = 'o'
        self.screen = screen
        self.x = x
        self.y = y

    @property
    def appearance(self):
        return self.symb

    def kill(self):
        self.screen.end_game()

