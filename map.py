import re
from pygame import Rect
from gconstants import *
from modifyfiles import *
from wall import *
from display import *


class Map(object):
    def __init__(self, File, Tileset):
        self.file = File
        self._map = {}
        self.mChange = []
        self.size = (0, 0)
        self.res = 0
        self.load()
        self.rect = pygame.Rect(0, 0, self.size[0] * res, self.size[1] * res)

        self.tileset = pygame.transform.scale(ModifyFiles().loadImage(Tileset), (res, res * TILE_SET_LENGTH)).convert()
        self.transColor = self.tileset.get_at((0, 0))
        self.acmap = pygame.surface.Surface((self.size[0] * res, self.size[1] * res))
        self.acmap.set_colorkey(self.transColor)
        self.display = Display(self, self.acmap, self.acmap.get_rect(), False)

        for i in self._map.keys():
            self.mChange.append(i)
        self.initDrawMap()

    def __call__(self, x=None, y=None):  # in the future, you could use this to get rows and columns
        if x is not None and y is not None:
            return self._map[(x, y)]
        return self._map

    def load(self):
        fStr = ModifyFiles().openFile(self.file)
        items = re.split("\.", fStr)
        self.res = res / int(items[0])
        self.size = int(items[1]), int(items[2])
        tx, ty = 0, 0
        for i in re.finditer("\((\d+),(\d+),(\d+),(\d+),(\d+),(\d+),\)", items[3]):
            pos = [int(i) for i in i.group(1, 2, 3, 4, 5, 6)]
            self._map[(tx, ty)] = Wall((tx * 32, ty * 32, pos[2] * self.res, pos[3] * self.res, pos[4], pos[5]))
            ty += 1
            if ty >= self.size[1]:
                ty = 0
                tx += 1

    def save(self):
        s = ["%s.%s.%s." % (int(res / self.res), self.size[0], self.size[1])]
        [s.append("(%s,%s,%s,%s,%s,%s,)" % (self._map[tile].rect.x, self._map[tile].rect.y, int(self._map[tile].rect.w / self.res), int(self._map[tile].rect.h / self.res), self._map[tile].type, self._map[tile].tile)) for tile in sorted(self._map.keys())]
        ModifyFiles().saveFile(''.join(s), self.file)

    def initDrawMap(self):
        for i, e in self.mChange:
            self.acmap.blit(self.tileset, (i * res, e * res), (0, self._map[(i, e)].tile * res, res, res))

    def draw(self, surface, camera):
        if self.mChange:
            self.initDrawMap()
            self.mChange = []
        self.display(surface, camera, camera)
