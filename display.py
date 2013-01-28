import pygame
from animation import *
from modifyfiles import *
from gconstants import *


class Display(object):
    def __init__(self, Parent, Tileset, Size, Transparent, Anim=(False, 1)):
        self.parent = Parent.rect
        if isinstance(Tileset, str):
            image = ModifyFiles().loadImage(Tileset)
            self.image = pygame.surface.Surface((Size[2], Size[3]))
            self.image.blit(image, (0, 0))
        else:
            self.image = Tileset

        self.trans = Transparent
        if self.trans:
            self.transColor = self.image.get_at((0, 0))
            self.image.set_colorkey(self.transColor)

        if Anim[0]:
            if hasattr(Parent, "move"):
                self.animation = Animation(image, Anim[1], Parent)
            else:
                self.animation = Animation(image, Anim[1], None)

    def draw(self, surface, camera, arm=False):
        if hasattr(self, "animation"):
            self.animation.animate(1)
            if self.trans:
                self.image.set_colorkey(self.transColor)
        if arm == "menu":
            surface.blit(self.image, camera.rect)
        elif self.parent.colliderect(camera.rect):
            if arm:
                surface.blit(self.image, (0, 0, 0, 0), arm.rect)
            else:
                surface.blit(self.image, self.translate(self.parent, camera.rect))

    def translate(self, rect, Cam):
        return pygame.Rect(rect.x - Cam.x, rect.y - Cam.y, rect.w, rect.h)
