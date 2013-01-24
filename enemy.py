from pygame import Rect
from move import *
from collision import *
from display import *
from ai import *


class Enemy(Rect):
    def __init__(self, Size, Speed, Tileset, Level):
        Object.__init__(self, Size)
        self.level = Level
        self.move = Move(Speed, self)
        self.collision = Collision(self, Level, "enemy")
        self.display = Display(Tileset, self, Size, True, (True, 11))
        self.ai = AI("goomba", self, Level)
        self.dead = False

    def tick(self):
        self.ai.tick()

