from pygame import *
from map import *
from camera import *
from editor import *
from gconstants import *
from platform import *
from background import *

class Level(object):
    def __init__(self, Level):
        self.entities = []
        self.map = Map(self.tLEVELS[0], self.tLEVELS[1])
        for i in []:#self.map.objects:
            self.addEntity(i)
        self.camera = Camera((0, 0, screenSize[0] * res, screenSize[1] * res), (screenSize[0] * res / 2, screenSize[1] * res / 2, 1, 1), (self.map.size[0] * res, self.map.size[1] * res))
        self.editor = Editor(self.map, self.camera)
        self.input = Input(settings, "LEVEL", {K_e: "editor", K_LEFT: "left", K_RIGHT: "right", K_UP: "up", K_DOWN: "down"})
        self.input.setShortcut("keydown", "editor", self.showEditor)
        self.input.setShortcut("keydown", "left", self.moveRect)
        self.input.setShortcut("keydown", "right", self.moveRect)
        self.input.setShortcut("keydown", "up", self.moveRect)
        self.input.setShortcut("keydown", "down", self.moveRect)

    def moveRect(self, dir):
        if "left" == dir:
            self.position.x -= 4
        if "right" == dir:
            self.position.x -= 4
        if "up" == dir:
            self.position.x -= 4
        if "down" == dir:
            self.position.x -= 4

    def addEntity(self, id=False, entity=None):
        if entity:
            if not id:
                self.entities[self.entityId] = entity
                entity.id = self.entityId
                self.entityId += 1
            else:
                self.entities[id] = entity

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def get(self, entityId):
        return self.entities.get(entityId)

    def process(self, controller, input):
        for entity in self.entities:
            if not entity.dead:
                entity.tick()

    def render(self, surface):
        self.map.draw(surface, self.camera)
        for entity in self.entities:
            entity.display.draw(surface, self.camera)
        if self.editor.enabled:
            self.editor.draw(surface, self.camera)

    def showEditor(self):
        self.editor.enabled = not self.editor.enabled

    def tick(self, control, input):
        self.input.checkInput(input)
        if self.editor.enabled:
            self.editor.edit(input)
        self.process(control, input)
        self.camera.tick()
