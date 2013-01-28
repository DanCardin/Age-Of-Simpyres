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
        self.mChange = True
        self.rect = pygame.Rect(0, 0, self.size[0] * res, self.size[1] * res)
        self.display = Display(self, self.acmap, self.acmap.get_rect(), False)
        self.initDrawMap()

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
                self._map[(i, e)] = Wall((pos[0] * self.res, pos[1] * self.res, pos[2] * self.res, pos[3] * self.res, pos[4], pos[5]))

    def save(self):
        s = ["%s.%s.%s." % (int(res / self.res), self.size[0], self.size[1])]
        [[s.append("(%s,%s,%s,%s,%s,%s,)" % (e.rect.x, e.rect.y, int(e.rect.w / self.res), int(e.rect.h / self.res), e.type, e.tile)) for e in i] for i in self._map]
        ns = ''.join(s)
        ModifyFiles().saveFile(ns, self.file)

    def getType(self, x, y):
        return self._map.get((x, y)).type

    def setType(self, x, y, Type):
        self._map.get((x, y)).type = Type

    def getTile(self, x, y):
        return self._map.get((x, y)).Tile

    def setTile(self, x, y, Tile):
        self._map.get((x, y)).tile = tile

    def wallDim(self, x, y):
        return pygame.Rect(x * res, y * res, 32, 32)#pygame.Rect(x * res + self._map[x][y].rect.x, y * res + self._map[x][y].rect.y, self._map[x][y].rect.w, self._map[x][y].rect.h)

    def initDrawMap(self):
        for pos, tile in self._map.items():
            til = pygame.surface.Surface((res, res))
            til.blit(self.tileset, (0, -1 * tile.tile * res, res, res))
            self.acmap.blit(til, (pos[0] * res, pos[1] * res))

    def draw(self, surface, camera):
        if self.mChange:
            self.initDrawMap()
        self.display.draw(surface, camera, camera)
