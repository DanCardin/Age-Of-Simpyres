import pygame
from gconstants import *
from modifyfiles import *
from wall import *
from display import *


class Map(object):
    def __init__(self, File, Tileset):
        self.fileMod = ModifyFiles()
        self.size = ()
        self.res = 0
        self.__map = [[]]
        self.start = ()
        self.file = File
        self.tileset = pygame.transform.scale(self.fileMod.loadImage(Tileset), (res, res * TILE_SET_LENGTH)).convert()
        self.load(self.file)
        self.transColor = self.tileset.get_at((0, 0))
        self.acmap = pygame.surface.Surface((self.size[0] * res, self.size[1] * res))
        self.acmap.set_colorkey(self.transColor)
        self.mChange = True
        self.display = Display(self.acmap, Object((0, 0, self.size[0] * res, self.size[1] * res)), self.acmap.get_rect(), False)

    def load(self, filename):
        pos, walls, bg = [], [], []
        s = self.fileMod.openFile(filename)
        for i in range(3):
            poss = s.find(".")
            bg.append(int(s[:poss]))
            s = s[poss + 1:]
        tot, s = float(res) / float(bg[0]), s[1:]
        for i in range(bg[1]):
            walls.append([])
            for e in range(bg[2]):
                end = s.find(")")
                ns, s, pos = s[:end], s[end + 2:], []
                while len(ns) > 0:
                    com = ns.find(",")
                    pos.append(int(ns[:com]))
                    ns = ns[com + 1:]
                if pos[4] == 2:
                    star = (i * res, e * res)
                walls[i].append(Wall((pos[0] * tot, pos[1] * tot, pos[2] * tot, pos[3] * tot, pos[4], pos[5])))
        self.size, self.res, self.__map, self.start = (i + 1, e + 1), tot, walls, star

    def save(self):
        s = ["%s.%s.%s." % (int(res / self.res), self.size[0], self.size[1])]
        [[s.append("(%s,%s,%s,%s,%s,%s,)" % (e.rect.x, e.rect.y, int(e.rect.w / self.res), int(e.rect.h / self.res), e.type, e.tile)) for e in i] for i in self.__map]
        ns = ''.join(s)
        self.fileMod.saveFile(ns, self.file)

    def getType(self, x, y):
        if (x in range(self.size[0])) and (y in range(self.size[1])):
            return self.__map[x][y].type

    def setType(self, x, y, Type):
        if (x in range(self.size[0])) and (y in range(self.size[1])):
            self.__map[x][y].type = Type

    def getTile(self, x, y):
        if (x in range(self.size[0])) and (y in range(self.size[1])):
            return self.__map[x][y].tile

    def setTile(self, x, y, Tile):
        if (x in range(self.size[0])) and (y in range(self.size[1])):
            self.__map[x][y].tile = Tile

    def wallDim(self, x, y):
        if (x in range(self.size[0])) and (y in range(self.size[1])):
            return pygame.Rect(x * res + self.__map[x][y].rect.x, y * res + self.__map[x][y].rect.y, self.__map[x][y].rect.w, self.__map[x][y].rect.h)

    def initDrawMap(self):
        for i in range(self.size[0]):
            for e in range(self.size[1]):
                til = pygame.surface.Surface((res, res))
                til.blit(self.tileset, (0, -1 * self.__map[i][e].tile * res, res, res))
                self.acmap.blit(til, (i * res, e * res))

    def draw(self, surface, camera):
        if self.mChange:
            self.initDrawMap()
        self.display.draw(surface, camera, camera.rect)
