from objects.base_object import BaseObject


class VoidObject(BaseObject):
    """
    Object which represents emptiness
    """
    def __init__(self, x, y):
        self.symb = '.'
        self.x = x
        self.y = y

    @property
    def appearance(self):
        return self.symb
