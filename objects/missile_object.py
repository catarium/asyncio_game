import asyncio
from typing import Callable

from objects.base_object import BaseObject
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen.screen import Screen


class MissileObject(BaseObject):
    """
    Object which represents the enemy
    """
    def __init__(self, screen: 'Screen', x: int, y: int, direction: Callable):
        self.symb = '!'
        self.screen = screen
        self.direction = direction
        self.x = x
        self.y = y
        self.screen.set_obj(x, y, self)
        self.alive = True

    @property
    def appearance(self):
        return self.symb

    def kill(self):
        self.alive = False

    def make_step(self):
        new_x, new_y = self.direction(self.x, self.y)
        if self.screen.move_object(new_x, new_y, self):
            self.x = new_x
            self.y = new_y

    async def start_acting(self):
        while self.alive:
            self.make_step()
            await asyncio.sleep(0.05)

