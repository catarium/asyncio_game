import asyncio

from objects.base_object import BaseObject
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen.screen import Screen


class EnemyObject(BaseObject):
    """
    Object which represents the enemy
    """
    def __init__(self, screen: 'Screen', x: int, y: int):
        self.symb = 'П'
        self.screen = screen
        self.x = x
        self.y = y
        self.screen.set_obj(x, y, self)
        self.alive = True

    def kill(self):
        self.alive = False

    @property
    def appearance(self):
        return self.symb

    def make_step(self):
        new_y = self.y + 1
        if self.screen.move_object(self.x, new_y, self):
            self.y = new_y

    async def start_acting(self):
        while self.alive:
            self.make_step()
            await asyncio.sleep(1)
