import asyncio

from objects.base_object import BaseObject
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from screen.screen import Screen


class SelfGuidedMissileObject(BaseObject):
    """
    Object which represents a self guided missile
    """
    def __init__(self, screen: 'Screen', x: int, y: int, target: BaseObject):
        self.symb = '#'
        self.screen = screen
        self.target = target
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
        """
        follows target by the closest possible way
        """
        new_x = self.x
        new_y = self.y
        if self.target.cords[0] > self.x:
            new_x = self.x + 1
        elif self.target.cords[0] < self.x:
            new_x = self.x - 1
        if self.target.cords[1] > self.y:
            new_y = self.y + 1
        elif self.target.cords[1] < self.y:
            new_y = self.y - 1
        if self.screen.move_object(new_x, new_y, self):
            self.x = new_x
            self.y = new_y

    async def start_acting(self):
        while self.alive:
            self.make_step()
            await asyncio.sleep(0.05)
