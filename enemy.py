from pygame import Rect
from move import *
from collision import *
from display import *
from ai import *


class Enemy(object):
    def __init__(self, Size, Speed, Tileset, Level):
        self.rect = Rect(Size)
        self.level = Level
        self.move = Move(Speed, self)
        self.move.moveSpeed((1, 1))
        self.collision = Collision(self, Level, "enemy")
        self.dir = (0, 0)
        self.display = Display(self, Tileset, Size, True, (True, 11))
        self.ai = AI("goomba", self, Level)
        self.dead = False

    def tick(self):
        if not self.dead:
            mRes = self.move.move()
            self.ai.tick(mRes)

            if self.move.speed[0] > 0:
                self.dir = (1, 0)
            if self.move.speed[0] < 0:
                self.dir = (-1, 0)
            if self.move.speed[1] > 0:
                self.dir = (0, 1)
            if self.move.speed[1] < 0:
                self.dir = (0, -1)
            if self.move.speed == (0,0):
                self.dir = (0, 0)

            for i in mRes:
                if i[0] == "bullet":
                    self.dead = True
