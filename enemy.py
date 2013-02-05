from pygame import *
from move import *
from collision import *
from display import *
from ai import *
from input import *


class Enemy(object):
    def __init__(self, Size, Speed, Tileset, Level):
        self.rect = Rect(Size)
        self.level = Level
        self.collision = Collision(self, "enemy")
        self.move = Move(self, Speed)
        self.move.moveSpeed((1, 1))
        self.dir = (0, 0)
        self.display = Display(self, Tileset, Size, True, (True, 11))
        self.ai = AI("goomba", self, Level)
        self.dead = False

        self.input = Input(None, "ENEMY")
        self.input.setShortcut(KEYDOWN, K_a, "left", self.move.moveSpeed, (-1, None))
        self.input.setShortcut(KEYDOWN, K_d, "right", self.move.moveSpeed, (1, None))
        self.input.setShortcut(KEYDOWN, K_w, "up", self.move.moveSpeed, (None, -1))
        self.input.setShortcut(KEYDOWN, K_s, "down", self.move.moveSpeed, (None, 1))
        self.input.setShortcut(KEYUP, K_a, "left", self.move.moveSpeed, (0, None))
        self.input.setShortcut(KEYUP, K_d, "right", self.move.moveSpeed, (0, None))
        self.input.setShortcut(KEYUP, K_w, "up", self.move.moveSpeed, (None, 0))
        self.input.setShortcut(KEYUP, K_s, "down", self.move.moveSpeed, (None, 0))

    def tick(self, input, mRes):
        self.input(input)
        if not self.dead:
            #self.ai.tick(mRes)

            if self.move.speed[0] > 0:
                self.dir = (1, 0)
            if self.move.speed[0] < 0:
                self.dir = (-1, 0)
            if self.move.speed[1] > 0:
                self.dir = (0, 1)
            if self.move.speed[1] < 0:
                self.dir = (0, -1)
            if self.move.speed == [0, 0]:
                self.dir = (0, 0)

            for i in mRes:
                if i[0] == 4:
                    self.dead = True
