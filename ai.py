import itertools


class AI(object):
    def __init__(self, Type, Parent, Level):
        self.parent = Parent
        self.level = Level
        self.type = Type

    def tick(self):
        if not self.parent.dead:
            if self.type == "goomba":
                self = self.parent
                self.gravity.tick()
                mRes = self.move.move()

                conditions = list(itertools.product(*[[1, "enemy", "char"], ["left", "right"]]))
                if [i for i in conditions if i in mRes]:
                    self.move.speed[0] *= -1

                conditions = list(itertools.product(*[[1, "enemy", "char"], ["top", "bottom"]]))
                if [i for i in conditions if i in mRes]:
                    self.move.speed[1] = 0

                for i in mRes:
                    if i[0] == "bullet":
                        self.parent.dead = True
