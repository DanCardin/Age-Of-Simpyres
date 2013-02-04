from pygame import display, event, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, K_m, K_r, K_e, QUIT
from menu import *
from level import *


class Game(object):
    def __init__(self, Type, LevelFile, LevelTileset):
        self.type = Type
        self.resize((screenSize[0] * res, screenSize[1] * res))
        self.levelFile = LevelFile
        self.levelTileset = LevelTileset
        self.level = Level(LevelFile, LevelTileset)
        self.enabled = False
        self.on = True
        self.size = (screenSize[0] * res, screenSize[1] * res)

        self.menu = Menu((screenSize[0] * res / 2 - 50, screenSize[1] * res / 2 - 100), True)
        self.menu.append((-25, -100, 150, 100), ("Pygame Game!", "gamename"), (None, ""), ((0, 0, 0), (0, 0, 0), (155, 150, 0)))
        self.menu.append((0, 0, 100, 48), ("Resume",), self.resume)
        self.menu.append((0, 50, 100, 48), ("Start",), self.restart)
        self.menu.append((0, 100, 100, 48), ("Settings",), self.settings)
        self.menu.append((0, 150, 100, 48), ("Exit",), self.exit)

        self.input = Input(settings, "GAME")
        self.input.setShortcut(KEYDOWN, K_m, "menu", self.showMenu)
        self.input.setShortcut(KEYDOWN, K_r, "restart", self.restart)
        self.input.setShortcut(KEYDOWN, K_e, "resize", self.togEditor)
        if not self.input.k:
            self.input.setKeys()
        #self.restart()

    def togEditor(self):
        if self.enabled:
            self.resize((self.size[0], self.size[1] + 2 * res * (not self.level.editorEnabled)))

    def resize(self, size):
        self.surface = display.set_mode(size)
        display.set_caption(gameName)

    def resume(self):
        self.enabled = True

    def restart(self):
        self.enabled = True
        self.level = Level(self.levelFile, self.levelTileset)

    def showMenu(self):
        self.enabled = not self.enabled

    def settings(self):
        """"""

    def win(self):
        self.on = False

    def exit(self):
        self.on = False

    def getEvents(self):
        result = []
        for even in event.get():
            if even.type is KEYDOWN or even.type is KEYUP:
                result.append((even.type, even.key))
            if even.type is QUIT:
                self.exit()
            if even.type is MOUSEBUTTONDOWN or even.type is MOUSEBUTTONUP:
                result.append((even.type, even.pos))
            if even.type is MOUSEMOTION:
                result.append((even.type, even.pos))
        return result

    def tick(self):
        self.surface.fill(0)
        inputs = self.getEvents()
        self.input(inputs)

        if self.enabled:
            if self.on:
                self.level.tick("name", inputs)
            else:
                self.win()
            self.level.render(self.surface)
        else:
            self.menu.tick(inputs)
            self.menu.draw(self.surface)
