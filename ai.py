import itertools


class AI(object):
    def __init__(self, Type, Parent, Level):
        self.parent = Parent
        self.level = Level
        self.type = Type

    def tick(self, mRes):
        if self.type == "goomba":
            self = self.parent.move
            conditions = list(itertools.product(*[[1, "enemy"], ["left", "right"]]))
            if [i for i in conditions if i in mRes]:
                self.speed[0] *= -1
            conditions = list(itertools.product(*[[1, "enemy"], ["top", "bottom"]]))
            if [i for i in conditions if i in mRes]:
                self.speed[1] *= -1
