import asyncio
from typing import Callable

from objects.base_object import BaseObject
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen.screen import Screen


class BlockObject(BaseObject):
    """
    Object which represents a block
    """
    def __init__(self, screen: 'Screen', x: int, y: int):
        self.symb = '#'
        self.screen = screen
        self.x = x
        self.y = y

    @property
    def appearance(self):
        return self.symb
