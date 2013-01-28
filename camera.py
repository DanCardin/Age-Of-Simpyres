from pygame import Rect
from move import *


class Camera(Rect):
    def __init__(self, Size, Bounds, Res, Target=None):
        self.rect = Rect(Size)
        if Target:
            self.target = Target.rect
        else:
            self.target = None
        self.bounds = Rect(Bounds)
        self.res = Res.rect
        self.move = Move((8, 8), self)

    def reTarget(self, Target):
        self.target = Target.rect

    def resize(self, size):
        self.rect.w = size[0]
        self.rect.h = size[1]

    def tick(self):
        self.move.move()
        if not self.target == None:
            if self.rect.x > self.target.x - self.bounds.x:
                self.rect.x = self.target.x - self.bounds.x
            if self.rect.x < self.target.x + self.target.w + self.bounds.w - self.rect.w:
                self.rect.x = self.target.x + self.target.w + self.bounds.w - self.rect.w

            if (self.rect.x < 0) and (self.rect.x + self.rect.w > self.res.w):
                self.rect.x = self.target.x + self.target.w / 2 - self.rect.w / 2

            if self.rect.y > self.target.y - self.bounds.y:
                self.rect.y = self.target.y - self.bounds.y
            if self.rect.y < self.target.y + self.target.h + self.bounds.h - self.rect.h:
                self.rect.y = self.target.y + self.target.h + self.bounds.h - self.rect.h

            if (self.rect.y < 0) and (self.rect.y + self.rect.h > self.res.h):
                self.rect.y = self.target.y + self.target.h / 2 - self.rect.h / 2

        if self.rect.x < self.res.x:
            self.rect.x = self.res.x
        if self.rect.x + self.rect.w > self.res.w:
            self.rect.x = (self.res.w) - self.rect.w
        if self.rect.y < self.res.y:
            self.rect.y = self.res.y
        if self.rect.y + self.rect.h > self.res.h:
            self.rect.y = (self.res.h) - self.rect.h
