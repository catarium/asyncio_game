import asyncio
import os

from objects.base_object import BaseObject
from objects.void_object import VoidObject


class Screen:
    """
    Shows screen
    """
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.data = [[VoidObject(j, i) for j in range(width)] for i in range(height)]

    def render_frame(self) -> None:
        """
        Prints a frame of the screen
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        for r in self.data:
            print(' '.join(map(lambda x: x.appearance, r)))

    def set_obj(self, x: int, y: int, obj: BaseObject) -> bool:
        """
        Changes the object on certain cell
        :param x: cell index
        :param y: row index
        :param obj: object
        :return: success of the operation
        """
        try:
            if x > self.width - 1 or x < 0 or y < 0 or y > self.height - 1:
                return False
            self.data[y][x] = obj
        except IndexError:
            print(x, y)
        return True

    def move_object(self, x: int, y: int, obj: BaseObject) -> bool:
        """
        Moves the object to the certain cell by replacing previous position with void
        :param x: cell index
        :param y: row index
        :param obj: onbject
        :return: success of the operation
        """
        res = self.set_obj(x, y, obj)
        if not res:
            return res
        self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))
        return res

    async def start_show(self):
        """
        Constantly renders frames.
        Awaits sleep every time.
        """
        while True:
            self.render_frame()
            await asyncio.sleep(0.01)
