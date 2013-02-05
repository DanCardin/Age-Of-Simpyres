import pygame
from math import floor


class Animation(object):
    def __init__(self, Image, TLength, Parent):
        self.parent = Parent
        self.tLength = TLength
        self.anim = {"up": [], "down": [], "left": [], "right": [], "stop": []}
        tx, ty = Image.get_width() / self.tLength, Image.get_height()
        self.currAnim = 0
        self.prevDir = 0
        for i in range(self.tLength):
            ta = pygame.surface.Surface((tx, ty))
            ta.blit(Image, (-i * tx, 0, i * tx + tx, ty))

            self.anim["up"].append(pygame.transform.rotate(ta, 0))
            self.anim["right"].append(pygame.transform.rotate(ta, -90))
            self.anim["down"].append(pygame.transform.rotate(ta, 180))
            self.anim["left"].append(pygame.transform.rotate(ta, 90))
            self.anim["stop"].append(pygame.transform.rotate(ta, 32 * i))

    def animate(self, direction):
        direc = self.parent.dir
        if direction > 0:
            if self.currAnim >= self.tLength or self.prevDir != direc:
                self.currAnim = 0
        else:
            if self.currAnim <= 0 or self.prevDir != direc:
                self.currAnim = self.tLength - 1
        if self.parent:
            if direc == (0, 0):
                img = self.anim["stop"][floor(self.currAnim)]
            elif direc == (-1, 0):
                img = self.anim["left"][floor(self.currAnim)]
            elif direc == (1, 0):
                img = self.anim["right"][floor(self.currAnim)]
            elif direc == (0, -1):
                img = self.anim["up"][floor(self.currAnim)]
            elif direc == (0, 1):
                img = self.anim["down"][floor(self.currAnim)]
        else:
            img = self.anim["right"][floor(self.currAnim)]
        self.currAnim += direction
        self.prevDir = direc
        self.parent.display.image = img
