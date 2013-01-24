import pygame
from animation import *
from modifyfiles import *
from gconstants import *


class Display(object):
    def __init__(self, Tileset, classs, Size, Transparent, Anim=(False, 1)):
        self.Class = classs
        if isinstance(Tileset, str):
            self.fileMod = ModifyFiles()
            image = self.fileMod.loadImage(Tileset)
            self.image = pygame.surface.Surface((Size[2], Size[3]))
            self.image.blit(image, (0, 0))
        else:
            self.image = Tileset

        self.trans = Transparent
        if self.trans:
            self.transColor = self.image.get_at((0, 0))
            self.image.set_colorkey(self.transColor)

        if Anim[0]:
            self.animation = Animation(image, Anim[1], self.Class)

    def draw(self, surface, camera, arm=False):
        if hasattr(self, "animation"):
            self.animation.animate(1)
            if self.trans:
                self.image.set_colorkey(self.transColor)
        rect = self.translate(self.Class.rect, camera.rect)
        if arm == "menu":
            surface.blit(self.image, rect)
        elif self.Class.rect.colliderect(camera):
            if arm:
                surface.blit(self.image, (0, 0, 0, 0), arm)
            else:
                surface.blit(self.image, rect)

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)
