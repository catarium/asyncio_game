import asyncio
import os
from sys import stdout

from objects.base_object import BaseObject
from objects.block_object import BlockObject
from objects.enemy_object import EnemyObject
from objects.home_object import HomeObject
from objects.missile_object import MissileObject
from objects.player_object import PlayerObject
from objects.self_guided_missile_object import SelfGuidedMissileObject
from objects.void_object import VoidObject


class Screen:
    """
    Shows screen
    """
    def __init__(self, height: int, width: int):
        self.alive = True
        self.height = height
        self.width = width
        self.counter = 0
        self.data = [[VoidObject(j, i) for j in range(width)] for i in range(height)]
        for i in range(1, width - 1):
            self.data[height - 2][i] = HomeObject(self, i, height - 2)
        for y in range(height):
            self.data[y][0] = BlockObject(self, 0, y)
            self.data[y][width - 1] = BlockObject(self, width - 1, y)
        for x in range(width):
            self.data[0][x] = BlockObject(self, x, 0)
            self.data[height - 1][x] = BlockObject(self, x, height - 1)

    def render_frame(self) -> None:
        """
        Prints a frame of the screen
        """
        string = f'Enemies killed: {self.counter}\n' + '\n'.join([' '.join([c.appearance for c in r]) for r in self.data])
        mult = '\033[A' * self.height
        stdout.write(f"{mult}\r{string}")
        stdout.flush()

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
        # I know it's bad, but I couldn't come up with anything else
        # Interactions between different objects
        if x > self.width - 1 or x < 0 or y < 0 or y > self.height - 1:
            return False
        if isinstance(self.data[y][x], VoidObject): # between any object and void
            res = self.set_obj(x, y, obj)
            if not res:
                return res
            self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))
        elif (isinstance(obj, PlayerObject) and (isinstance(self.data[y][x], MissileObject) or
                                                isinstance(self.data[y][x], SelfGuidedMissileObject))) or (
                isinstance(obj, MissileObject) or isinstance(obj, SelfGuidedMissileObject)) and isinstance(self.data[y][x], PlayerObject): # between missiles and player
            obj.kill()
            self.data[y][x].kill()
            self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))
            self.set_obj(x, y, VoidObject(x, y))
            res = True
        elif (isinstance(obj, EnemyObject) and (isinstance(self.data[y][x], MissileObject) or
                                                 isinstance(self.data[y][x], SelfGuidedMissileObject))) or (
                isinstance(obj, MissileObject) or isinstance(obj, SelfGuidedMissileObject)) and isinstance(self.data[y][x], EnemyObject): # between missiles and enemy
            obj.kill()
            self.data[y][x].kill()
            self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))
            self.set_obj(x, y, VoidObject(x, y))
            self.counter += 1
            res = True
        elif (isinstance(obj, EnemyObject) and isinstance(self.data[y][x], PlayerObject)) or (isinstance(obj, PlayerObject) and isinstance(self.data[y][x], EnemyObject)): # player and enemy
            obj.kill()
            self.data[y][x].kill()
            self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))
            self.set_obj(x, y, VoidObject(x, y))
            res = True
        elif isinstance(obj, EnemyObject) and isinstance(self.data[y][x], HomeObject): # enemy and block
            self.data[y][x].kill()
            return False
        elif isinstance(obj, PlayerObject) and isinstance(self.data[y][x], BlockObject): # block and player
            return False
        elif isinstance(obj, EnemyObject) or isinstance(self.data[y][x], EnemyObject): # enemy and block
            return False
        elif (isinstance(obj, MissileObject) or
              isinstance(obj, SelfGuidedMissileObject)) and isinstance(self.data[y][x], BlockObject): # missiles and block
            obj.kill()
            self.set_obj(obj.x, obj.y, VoidObject(obj.x, obj.y))

            return True
        else:
            res = False
        return res

    def end_game(self):
        self.alive = False

    async def start_show(self, player):
        """
        Constantly renders frames.
        Awaits sleep every time.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        while self.alive:
            self.render_frame()
            await asyncio.sleep(0.01)
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Game Over')
