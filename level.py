from pygame import *
from map import *
from camera import *
from editor import *
from gconstants import *
from enemy import *

class Level(object):
    def __init__(self, File, Tileset):
        self.entities = {}
        self.map = Map(File, Tileset)
        for i in []:#self.map.objects:
            self.addEntity(i)
        self.entityId = 0
        self.addEntity(entity=Enemy((64, 96, 20, 26), (4, 4), playerTileset, self))
        self.position = Rect(100, 100, 1, 1)
        self.camera = Camera((0, 0, screenSize[0] * res, screenSize[1] * res), (screenSize[0] * res / 2, screenSize[1] * res / 2, 1, 1), self.map)
        self.editor = Editor(self.map, self.camera)
        self.input = Input(settings, "LEVEL")
        self.input.setShortcut(K_e, "down", "editor", self.showEditor)
        self.input.setShortcut(K_LEFT, "down", "left", self.camera.move.moveSpeed, (-1, None))
        self.input.setShortcut(K_RIGHT, "down", "right", self.camera.move.moveSpeed, (1, None))
        self.input.setShortcut(K_UP, "down", "up", self.camera.move.moveSpeed, (None, -1))
        self.input.setShortcut(K_DOWN, "down", "down", self.camera.move.moveSpeed, (None, 1))
        self.input.setShortcut(K_LEFT, "up", "left", self.camera.move.moveSpeed, (0, None))
        self.input.setShortcut(K_RIGHT, "up", "right", self.camera.move.moveSpeed, (0, None))
        self.input.setShortcut(K_UP, "up", "up", self.camera.move.moveSpeed, (None, 0))
        self.input.setShortcut(K_DOWN, "up", "down", self.camera.move.moveSpeed, (None, 0))
        if not self.input.k:
            self.input.setKeys()

    def addEntity(self, id=None, entity=None):
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
        for entity in self.entities.values():
            if not entity.dead:
                entity.tick()

    def render(self, surface):
        self.map.draw(surface, self.camera)
        for entity in self.entities.values():
            entity.display.draw(surface, self.camera)
        if self.editor.enabled:
            self.editor.draw(surface, self.camera)

    def showEditor(self):
        self.editor.enabled = not self.editor.enabled

    def tick(self, control, input):
        self.input.checkInput(input)
        self.camera.tick()
        if self.editor.enabled:
            self.editor.edit(input)
        self.process(control, input)
