from abc import ABC, abstractmethod


class BaseObject:
    @abstractmethod
    def __init__(self, symb, x: int, y: int):
        self.symb = symb
        self.x = x
        self.y = y

    @property
    @abstractmethod
    def appearance(self):
        return self.symb
