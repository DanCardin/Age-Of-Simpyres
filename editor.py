from pygame import Rect, Surface, MOUSEBUTTONUP, MOUSEBUTTONDOWN
from gconstants import *
from display import *
from menu import *
from input import *


class Editor(pygame.Rect):
    def __init__(self, Map, Camera):
        self.rect = Rect(0, 0, Map.size[0] * res, Map.size[1] * res)
        self.map = Map
        self.camera = Camera.rect
        self.tileTile, self.tool, self.tileType = 0, 0, 1
        self.painting, self.collisionToggle = False, True
        self.mChange = []
        for i, e in self.map().keys():
            self.mChange.append((i, e))
        self._acmap = pygame.surface.Surface((self.rect.w, self.rect.h))
        self._acmap.set_alpha(75, pygame.RLEACCEL)
        self._acmap.set_colorkey((0, 0, 0))
        self.display = Display(self, self._acmap, self, False)
        self.create()

    def create(self):
        self.menu = Menu((0, screenSize[1] * res), False)
        self.menu.append((0, 0, 32, 32), ("Save",), self.map.save)
        self.menu.append((32, 0, 32, 32), ("Pen",), (self.updateTool, 0), Toggle=4)
        self.menu.append((64, 0, 32, 32), ("Box",), (self.updateTool, 1), Toggle=4)
        self.menu.append((96, 0, 32, 32), ("Tiles",), (self.updateType, -1), Toggle=1)
        self.menu.append((196, 0, 100, 32), ("Wall",), (self.updateType, 1), Toggle=1)
        self.menu.append((296, 0, 100, 32), ("Empty",), (self.updateType, 0), Toggle=1)
        self.menu.append((396, 0, 100, 32), ("Death",), (self.updateType, 4), Toggle=1)
        self.menu.append((500, 0, 100, 32), ("Collision",), self.toggleCollision, Toggle=3)
        self.menu.select("Pen").toggledOn = True
        self.menu.select("Wall").toggledOn = True
        for i in range(TILE_SET_LENGTH):
            surf = Surface((30, 30))
            surf.blit(self.map.tileset, (0, 0, res, res), (1, i * res, res - 2, res - 2))
            self.menu.append((32 * i, 32, 32, 32), ("", str(i)), (self.updateTile, i), Image=surf, Toggle=2)

    def updateTool(self, Tool):
        self.tool = Tool

    def updateType(self, Type):
        self.tileType = Type

    def updateTile(self, Tile):
        self.tileTile = Tile

    def toggleCollision(self):
        self.collisionToggle = not self.collisionToggle

    def pen(self, key):
        x, y = int((key[0] + self.camera.x) / res), int((key[1] + self.camera.y) / res)
        if 0 <= x <= screenSize[0] and 0 <= y <= screenSize[1]:
            if self.tileType == -1:
                self.map(x, y).tile = self.tileTile
            else:
                self.map(x, y).type = self.tileType
            self.mChange.append((x, y))
            self.map.mChange.append((x, y))

    def box(self, input):
        """self.mChange.append(box)"""

    def drawMap(self):
        for i, e in self.mChange:
            col = {0: (0, 0, 0), 1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 255), 4: (255, 0, 0)}[self.map(i, e).type]
            pygame.draw.rect(self._acmap, col,  (i * res, e * res, res, res))

    def draw(self, surface, camera):
        if self.collisionToggle:
            if self.mChange:
                self.drawMap()
                self.mChange = []
            self.display(surface, camera, camera)
        self.menu.draw(surface)

    def __call__(self, input):
        self.menu.tick(input)
        for event in input:
            if event[0] in [MOUSEBUTTONUP, MOUSEBUTTONDOWN]:
                self.painting = {pygame.MOUSEBUTTONDOWN: True, pygame.MOUSEBUTTONUP: False}.get(event[0])
            if self.painting:
                if self.tool == 0:
                    self.pen(event[1])
                elif self.tool == 1:
                    self.box(event)
