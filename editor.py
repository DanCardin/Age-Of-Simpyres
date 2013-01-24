import pygame
from gconstants import *
from display import *
from menu import *
from input import *


class Editor(Object):
    def __init__(self, Map, Camera):
        Object.__init__(self, (0, 0, Map.size[0] * res, Map.size[1] * res))
        self.map = Map
        self.camera = Camera
        self.brush = self.tool = self.modifier = 0
        self.bType = -1
        self.painting, self.menuShowing, self.enabled, self.mChange, self.tile = False, True, False, True, False
        self.acmap = pygame.surface.Surface((self.rect.w, self.rect.h))
        self.acmap.set_alpha(75, pygame.RLEACCEL)
        self.acmap.set_colorkey((0, 0, 0))
        self.display = Display(self.acmap, self, self.acmap.get_rect(), False)
        self.input = Input(settings, "EDIT", {pygame.K_l: "emenu", pygame.K_RETURN: "save", pygame.K_LCTRL: "start", pygame.K_LSHIFT: "end"})
        self.input.setShortcut("keydown", "emenu", self.toggleMenu)
        self.input.setShortcut("keydown", "save", self.map.save)
        self.input.setShortcut("keydown", "start", self.startBlock)
        self.input.setShortcut("keydown", "end", self.endBlock)
        self.create()

    def create(self):
        self.menu = Menu((0, screenSize[1] * res), False)
        self.menu.append((0, 0, 32, 32), "Save", "save",)
        self.menu.append((32, 0, 32, 32), "Pen", "pen", Image=False, Toggle=True, TGroup=0)
        self.menu.append((64, 0, 32, 32), "Box", "box", Image=False, Toggle=True, TGroup=0)
        self.menu.append((96, 0, 32, 32), "Tiles", "tiles", Image=False, Toggle=True, TGroup=1)
        self.menu.append((196, 0, 100, 32), "Wall", "wall", Image=False, Toggle=True, TGroup=1)
        self.menu.append((296, 0, 100, 32), "Empty", "empty", Image=False, Toggle=True, TGroup=1)
        self.menu.append((500, 0, 100, 32), "Collision", "collision", Image=False, Toggle=True, TGroup=3)
        self.menu.select("pen").togState = True
        self.menu.select("tiles").togState = True
        for i in range(TILE_SET_LENGTH):
            surf = pygame.surface.Surface((30, 30))
            surf.blit(self.map.tileset, pygame.Rect(-1, -i * res, res - 2, res - 2))
            self.menu.append((32 * i, 32, 32, 32), "", i, Image=surf, Toggle=True, TGroup=2)

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

    def startBlock(self):
        self.modifier = 1

    def endBlock(self):
        self.modifier = 2

    def handleMouse(self, event, input):
        return {pygame.MOUSEBUTTONDOWN: True, pygame.MOUSEBUTTONUP: False}.get(event)

    def handleMenu(self, action, input):
        self.modifier = 0
        if action == []:
            self.input.checkInput(input)
            for event, key in input:
                if not (event == pygame.KEYDOWN or event == pygame.KEYUP):
                    self.painting = self.handleMouse(event, key)

        if "pen" in action:
            self.tool = 0
        if "box" in action:
            self.tool = 1
        if "tiles" in action:
            self.bType = -1

        if "empty" in action:
            self.bType = 0
        if "death" in action:
            self.bType = 4
        if "wall" in action:
            self.menu.items[4].update(OColor=((0, 0, 255)))
            self.bType = 1

        if "save" in action:
            self.map.save()
        if "collision" in action:
            self.menuShowing = not self.menuShowing

        for i in range(TILE_SET_LENGTH):
            if i in action:
                self.brush = i

    def edit(self, input):
        mPos = pygame.mouse.get_pos()  # fix it, it doesnt need this because "input" already has the mouse pos
        self.handleMenu(self.menu.tick(input, mPos), input)
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
            self.display.draw(surface, camera, camera.rect)
        self.menu.draw(surface)
