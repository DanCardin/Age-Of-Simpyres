from pygame import Rect, Surface, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from gconstants import *
from display import *
from menu import *
from input import *


class Editor(pygame.Rect):
    def __init__(self, Map, Camera):
        self.rect = Rect(0, 0, Map.size[0] * res, Map.size[1] * res)
        self.map = Map
        self.camera = Camera
        self.brush = self.tool = self.modifier = 0
        self.bType = -1
        self.painting, self.menuShowing, self.enabled, self.mChange, self.tile = False, True, False, True, False
        self.acmap = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.acmap.set_alpha(75, pygame.RLEACCEL)
        self.acmap.set_colorkey((0, 0, 0))
        self.display = Display(self, self.acmap, self, False)
        self.create()

    def create(self):
        self.menu = Menu((0, screenSize[1] * res), False)
        self.menu.append((0, 0, 32, 32), ("Save",), (self.map.save))
        self.menu.append((32, 0, 32, 32), ("Pen",), (self.tool, 0), Toggle=0)
        self.menu.append((64, 0, 32, 32), ("Box",), (self.tool, 1), Toggle=0)
        self.menu.append((96, 0, 32, 32), ("Tiles",), (self.bType, -1), Toggle=1)
        self.menu.append((196, 0, 100, 32), ("Wall",), (self.bType, 1), Toggle=1)
        self.menu.append((296, 0, 100, 32), ("Empty",), (self.bType, 0), Toggle=1)
        self.menu.append((396, 0, 100, 32), ("Death",), (self.bType, 4), Toggle=1)
        self.menu.append((500, 0, 100, 32), ("Collision",), (self.toggleMenu), Toggle=3)
        self.menu.select("Pen").togState = True
        self.menu.select("Wall").togState = True
        for i in range(TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(self.map.tileset, pygame.Rect(-1, -i * res, res - 2, res - 2))
            self.menu.append((32 * i, 32, 32, 32), ("", str(i)), (self.brush, i), Image=surf, Toggle=2)

    def pen(self, key):
        tile = (int((key[0] + self.camera.rect.x) / res), int((key[1] + self.camera.rect.y) / res))
        print(self.bType)
        print(tile)
        if self.bType == -1:
            self.map.setTile(tile[0], tile[1], self.brush)
        elif self.bType >= 0:
            self.map.setType(tile[0], tile[1], self.bType)

    def box(self, input, key):
        if not hasattr(self, "gen"):
            self.gen = 1
        for event, keyy in input:
            if event == pygame.MOUSEBUTTONDOWN:
                self.gen = {-1: 1, 1: -1}[self.gen]

    def toggleMenu(self):
        self.menuShowing = not self.menuShowing

    def edit(self, input):
        if input:
            if input[0] in [MOUSEBUTTONUP, MOUSEBUTTONDOWN]:
                self.painting = {pygame.MOUSEBUTTONDOWN: True, pygame.MOUSEBUTTONUP: False}.get(input[0])
                self.menu.tick(input)
        if self.painting:
            self.mChange = True
            if self.tool == 0:
                self.pen(mPos)
            elif self.tool == 1:
                self.box(input, mPos)

    def drawMap(self):
        for i in range(self.map.size[0]):
            for e in range(self.map.size[1]):
                col = {0: (0, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 255), 4: (255, 0, 0)}[self.map.getType(i, e)]
                if col != self.map.transColor:
                    pygame.draw.rect(self.acmap, col,  (i * res, e * res, res, res))

    def draw(self, surface, camera):
        if self.mChange:
            self.drawMap()
            self.mChange = False
        if self.menuShowing:
            self.display.draw(surface, camera, camera)
        self.menu.draw(surface)
