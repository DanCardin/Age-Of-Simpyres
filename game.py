import pygame
try:
    import cpickle as pickle
except:
    import pickle
from world import *
from menu import *
from server import *
from client import *


class Game(object):
    def __init__(self, Type, Levels):
        self.levAttr = Levels
        self.resize((screenSize[0] * res, screenSize[1] * res))
        self.world = World(self.levAttr)
        self.enabled = False
        self.on = True
        self.size = (screenSize[0] * res, screenSize[1] * res)
        self.type = Type
        if "server" in self.type:
            #self.server = Server(self.world.level, "", 9999)
            self.server = Server(self.world.level, "localhost", 9999)
        if "client" in self.type:
            self.client = Client(self.world.level, b"dan", "localhost", 9999)
            self.client.connect()

        text = ['Resume', 'Start', 'Settings', 'Exit']
        self.menu = Menu((screenSize[0] * res / 2 - 50, screenSize[1] * res / 2 - 50 * len(text) / 2), True)
        self.menu.append((-25, -100, 150, 100), "Pygame Game!", "", (0, 0, 0), (0, 0, 0), (155, 150, 0))
        for i in range(0, len(text)):
            self.menu.append((0, 50 * i, 100, 48), text[i], text[i].lower())

        self.input = Input(settings, "GAME", {pygame.K_m: "menu", pygame.K_r: "restart", pygame.K_e: "resize"})
        self.input.setShortcut("keydown", "menu", self.showMenu)
        self.input.setShortcut("keydown", "restart", self.restart)
        self.input.setShortcut("keydown", "resize", self.togEditor)

        if "client" in self.type:
            self.restart()

    def togEditor(self):
        self.resize((self.size[0], self.size[1] + 2 * res * (not self.world.level.editor.enabled)))

    def resize(self, size):
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(gameName)

    def resume(self):
        if self.world != 0:
            self.enabled = True
        else:
            self.start()
        self.menu.enabled = False

    def restart(self):
        self.menu.enabled = False
        self.enabled = True
        self.world.level.restart()
        if "server" in self.type:
            self.server.spawnPlayers()

    def showMenu(self):
        self.menu.enabled = not self.menu.enabled
        self.enabled = not self.enabled

    def handleMenu(self, action):
        if 'resume' in action:
            self.resume()
        elif 'start' in action:
            self.restart()
        elif 'settings' in action:
            """"""  # settings eventually
        elif 'exit' in action:
            self.exit()

    def win(self):
        self.on = False

    def exit(self):
        self.on = False

    def getEvents(self):
        re = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                re.append((event.type, event.key))
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                re.append((event.type, event.pos))
        return re

    def tick(self):
        self.surface.fill(0)
        inputs = []
        name = ""

        if "client" in self.type:
            getInput = self.getEvents()
            for i in getInput:
                self.client.send(i)

        if "server" in self.type:
            for name, inp in self.server.receive():
                inputs.append(inp)

        if "server" in self.type:
            self.input.checkInput(inputs)
            self.handleMenu(self.menu.tick(inputs, pygame.mouse.get_pos()))
            if self.enabled:
                if not self.world.won:
                    self.world.tick(name, inputs)
                else:
                    self.win()
            tmp = {}
            for key, value in self.world.level.entities.items():
                tmp[key] = value.rect
            self.server.send(tmp)

        if "client" in self.type:
            for key, value in self.client.receive().items():
                self.world.level.entities[key].rect = value
            self.world.render(self.surface)
            self.menu.draw(self.surface)

