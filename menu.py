from object import *
from display import *
from gconstants import *
import main
import pygame


class Menu(object):
    def __init__(self, Pos, Showing):
        self.pos = Pos
        self.items = {}
        self.enabled = Showing

    def append(self, Rect, Text, key, RColor=(255, 0, 0), OColor=(0, 0, 255), TColor=(0, 255, 0), Image=False, Toggle=False, TGroup=None):
        self.items[key] = MenuItem(key, Rect, RColor, OColor, Text, TColor, Image, Toggle, TGroup)

    def animate(self, animation):
        """"""

    def select(self, key):
        return self.items.get(key)

    def tick(self, input, mpos):
        t = []
        if self.enabled:
            for key, item in self.items.items():
                tmp = len(t)
                if len(input) > 0:
                    for event, key in input:
                        eTick = item.tick(event, self.pos, mpos)
                        if eTick != None:
                            t.append(eTick)
                if len(t) > tmp:
                    if len(self.items) == 1:
                        self.items[0].togState = not self.items[0].togState
                    else:
                        for key2, e in self.items.items():
                            if e.toggle:
                                if e.tGroup == item.tGroup:
                                    e.togState = {True: 1, False: 0}[e.togState == 2]
                item.tick(0, self.pos, mpos)
        return t

    def draw(self, surface):
        if self.enabled:
            for key, item in self.items.items():
                item.display.draw(surface, Object((self.pos[0] * -1, self.pos[1] * -1, screenSize[0] * res, screenSize[1] * res)), "menu")


class MenuItem(Object):
    def __init__(self, Action, Rect, RColor, OColor, Text, TColor, Image, Toggle, TGroup):
        Object.__init__(self, Rect)
        self.action = Action
        self.images = [pygame.surface.Surface((self.rect.w, self.rect.h)), pygame.surface.Surface((self.rect.w, self.rect.h))]
        self.tGroup = TGroup
        self.toggle = Toggle
        if self.toggle:
            self.togState = 0
        self.display = Display(self.images[0], self, self.images[0].get_rect, False)

        self.rcolor = RColor
        self.ocolor = OColor
        self.tcolor = TColor
        self.text = Text
        self.image = Image
        self.update()

    def update(self, Rect=None, RColor=None, OColor=None, Text=None, TColor=None, Image=None):
        if Rect == None:
            Rect = self.rect
        if RColor == None:
            RColor = self.rcolor
        if OColor == None:
            OColor = self.ocolor
        if Text == None:
            Text = self.text
        if TColor == None:
            TColor = self.tcolor
        if Image == None:
            Image = self.image

        colors = [RColor, OColor]
        for i in range(len(colors)):
            self.images[i].fill(colors[i])
            if Text:
                if main.android:
                    text = pygame.surface.Surface((0, 0))
                else:
                    text = pygame.font.Font(None, 25).render(Text, 1, TColor)
                self.images[i].blit(text, ((self.images[i].get_width() / 2) - (text.get_width() / 2), (self.images[i].get_height() / 2) - (text.get_height() / 2)))
            if Image != False:
                self.images[i].blit(Image, (1, 1))

    def move(self, vect):
        self.rect.x += self.vect[0]
        self.rect.y += self.vect[1]

    def grow(self, dx, dy):
        self.rect.w += dx
        self.rect.h += dy

    def tick(self, input, menu, mPos):
        collide = pygame.Rect(menu[0] + self.rect.x, menu[1] + self.rect.y, self.rect.w, self.rect.h).collidepoint(mPos[0], mPos[1])
        self.display.image = self.images[collide]
        if self.toggle:
            if self.togState:
                self.display.image = self.images[1]
        if input == pygame.MOUSEBUTTONDOWN:
            if collide:
                if self.toggle:
                    self.togState = 2
                return self.action
