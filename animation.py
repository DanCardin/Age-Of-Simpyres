import pygame
from math import floor


class Animation(object):
    def __init__(self, Image, TLength, Parent):
        self.parent = Parent
        self.tLength = TLength
        self.anim = {"up": [], "down": [], "left": [], "right": [], "stop": []}
        tx, ty = Image.get_width() / self.tLength, Image.get_height()
        self.currAnim = 0
        self.dir = Parent.dir
        self.prevDir = 0
        for i in range(self.tLength):
            ta = pygame.surface.Surface((tx, ty))
            ta.blit(Image, (-i * tx, 0, i * tx + tx, ty))
            if i == 0:
                self.anim["right"].append(ta)
                self.anim["down"].append(ta)
                self.anim["left"].append(pygame.transform.flip(ta, 1, 0))
                self.anim["up"].append(pygame.transform.flip(ta, 1, 0))
            else:
                self.anim["stop"].append(ta)
                self.anim["stop"].append(pygame.transform.flip(ta, 1, 0))

    def animate(self, direction):
        img = self.parent.display.image
        dir = direction * .5
        if self.parent:
            if self.currAnim >= self.tLength:
                self.currAnim = 0
            if self.dir != self.dir:
                self.currAnim = 0
            if self.dir == (0, 0):
                img = self.anim["stop"][self.currAnim]
            if self.dir == (-1, 0):
                img = self.anim["left"][self.currAnim]
            if self.dir == (1, 0):
                img = self.anim["right"][self.currAnim]
            if self.dir == (0, -1):
                img = self.anim["up"][self.currAnim]
            if self.dir == (0, 1):
                img = self.anim["down"][self.currAnim]
            self.currAnim += 1
        img = self.anim["right"][0]
        self.prevDir = self.dir
