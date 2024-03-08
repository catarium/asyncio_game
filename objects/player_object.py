from objects.base_object import BaseObject
from screen.screen import Screen


class PlayerObject(BaseObject):
    """
    Object which represents the player
    """
    def __init__(self, screen: Screen, x: int, y: int):
        self.symb = '&'
        self.screen = screen
        self.x = x
        self.y = y
        self.screen.set_obj(x, y, self)

    @property
    def appearance(self):
        return self.symb

    def move_up(self):
        if self.screen.move_object(self.x, self.y - 1, self):
            self.y -= 1

    def move_down(self):
        if self.screen.move_object(self.x, self.y + 1, self):
            self.y += 1

    def move_right(self):
        if self.screen.move_object(self.x + 1, self.y, self):
            self.x += 1

    def move_left(self):
        if self.screen.move_object(self.x - 1, self.y, self):
            self.x -= 1
