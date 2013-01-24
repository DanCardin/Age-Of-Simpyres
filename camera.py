import pygame
from object import *


class Camera(Object):
    def __init__(self, Size, Bounds, Res, Target=None):
        Object.__init__(self, Size)
        if Target:
            self.target = Target.rect
        else:
            self.target = pygame.Rect(0,0,0,0)
        self.bounds = pygame.Rect(Bounds)
        self.res = Res

    def reTarget(self, Target):
        self.target = Target.rect

    def resize(self, size):
        self.rect.w = size[0]
        self.rect.h = size[1]

    def tick(self):
        if self.rect.x > self.target.x - self.bounds.x:
            self.rect.x = self.target.x - self.bounds.x
        if self.rect.x < self.target.x + self.target.w + self.bounds.w - self.rect.w:
            self.rect.x = self.target.x + self.target.w + self.bounds.w - self.rect.w

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + self.rect.w > self.res[0]:
            self.rect.x = (self.res[0]) - self.rect.w
        if (self.rect.x < 0) and (self.rect.x + self.rect.w > self.res[0]):
            self.rect.x = self.target.x + self.target.w / 2 - self.rect.w / 2

        if self.rect.y > self.target.y - self.bounds.y:
            self.rect.y = self.target.y - self.bounds.y
        if self.rect.y < self.target.y + self.target.h + self.bounds.h - self.rect.h:
            self.rect.y = self.target.y + self.target.h + self.bounds.h - self.rect.h

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.h > self.res[1]:
            self.rect.y = (self.res[1]) - self.rect.h
        if (self.rect.y < 0) and (self.rect.y + self.rect.h > self.res[1]):
            self.rect.y = self.target.y + self.target.h / 2 - self.rect.h / 2
