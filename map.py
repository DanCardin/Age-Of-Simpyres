from pygame import Rect
from gconstants import *
from modifyfiles import *
from wall import *
from display import *


class Map(object):
    def __init__(self, File, Tileset):
        self.size = (0, 0)
        self.res = 0
        self._map = {}
        self.file = File
        self.tileset = pygame.transform.scale(ModifyFiles().loadImage(Tileset), (res, res * TILE_SET_LENGTH)).convert()
        self.load(self.file)
        self.transColor = self.tileset.get_at((0, 0))
        self.acmap = pygame.surface.Surface((self.size[0] * res, self.size[1] * res))
        self.acmap.set_colorkey(self.transColor)
        self.rect = pygame.Rect(0, 0, self.size[0] * res, self.size[1] * res)
        self.display = Display(self, self.acmap, self.acmap.get_rect(), False)
        self.mChange = []
        for i in self._map.keys():
            self.mChange.append(i)
        self.initDrawMap()

    def __call__(self, x=None, y=None):  # in the future, you could use this to get rows and columns
        if x is not None and y is not None:
            return self._map[(x, y)]
        return self._map

    def load(self, filename):
        fStr = ModifyFiles().openFile(filename)
        pos, bg = [], []
        for i in range(3):
            poss = fStr.find(".")
            bg.append(int(fStr[:poss]))
            fStr = fStr[poss + 1:]
        self.res, fStr = float(res) / bg[0], fStr[1:]
        self.size = (bg[1], bg[2])
        for i in range(self.size[0]):
            for e in range(self.size[1]):
                end = fStr.find(")")
                ns, fStr, pos = fStr[:end], fStr[end + 2:], []
                while len(ns) > 0:
                    com = ns.find(",")
                    pos.append(int(ns[:com]))
                    ns = ns[com + 1:]
                #self._map[(i, e)] = Wall((pos[0] * self.res, pos[1] * self.res, pos[2] * self.res, pos[3] * self.res, pos[4], pos[5]))
                self._map[(i, e)] = Wall((i * 32, e * 32, pos[2] * self.res, pos[3] * self.res, pos[4], pos[5]))

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
