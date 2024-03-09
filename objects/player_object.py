import asyncio

from objects.base_object import BaseObject
from typing import TYPE_CHECKING

from objects.missile_object import MissileObject

if TYPE_CHECKING:
    from screen.screen import Screen


class PlayerObject(BaseObject):
    """
    Object which represents the player
    """
    def __init__(self, screen: 'Screen', x: int, y: int):
        self.symb = 'W'
        self.screen = screen
        self.x = x
        self.y = y
        self.alive = True
        self.screen.set_obj(x, y, self)

    @property
    def cords(self):
        return self.x, self.y

    @property
    def appearance(self):
        return self.symb

    def kill(self):
        self.alive = False

    async def shoot(self):
        cords = (self.x, self.y - 1)
        missile = MissileObject(self.screen, cords[0], cords[1], lambda x, y: (x, y - 1))
        asyncio.create_task(missile.start_acting())
        self.screen.set_obj(cords[0], cords[1], missile)

    def move_up(self):
        if self.alive and self.screen.move_object(self.x, self.y - 1, self):
            self.y -= 1

    def move_down(self):
        if self.alive and self.screen.move_object(self.x, self.y + 1, self) :
            self.y += 1

    def move_right(self):
        if self.alive and self.screen.move_object(self.x + 1, self.y, self):
            self.x += 1

    def move_left(self):
        if self.alive and self.screen.move_object(self.x - 1, self.y, self):
            self.x -= 1
