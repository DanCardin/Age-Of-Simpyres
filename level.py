from pygame import KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_e
from map import *
from camera import *
from editor import *
from gconstants import *
from enemy import *


class Level(object):
    def __init__(self, File, Tileset):
        self.entities = {}
        self.map = Map(File, Tileset)
        for i in []:  # self.map.objects:
            self.addEntity(i)
        self.entityId = 0
        self.addEntity(entity=Enemy((64, 96, 20, 26), (4, 4), playerTileset, self))
        self.position = Rect(100, 100, 1, 1)
        self.camera = Camera((0, 0, screenSize[0] * res, screenSize[1] * res), (screenSize[0] * res / 2, screenSize[1] * res / 2, 1, 1), self.map)
        self.editor = Editor(self.map, self.camera)
        self.editorEnabled = False
        self.input = Input(settings, "LEVEL")
        self.input.setShortcut(KEYDOWN, K_e, "editor", self.toggleEditor)
        self.input.setShortcut(KEYDOWN, K_LEFT, "left", self.camera.move.moveSpeed, (-1, None))
        self.input.setShortcut(KEYDOWN, K_RIGHT, "right", self.camera.move.moveSpeed, (1, None))
        self.input.setShortcut(KEYDOWN, K_UP, "up", self.camera.move.moveSpeed, (None, -1))
        self.input.setShortcut(KEYDOWN, K_DOWN, "down", self.camera.move.moveSpeed, (None, 1))
        self.input.setShortcut(KEYUP, K_LEFT, "left", self.camera.move.moveSpeed, (0, None))
        self.input.setShortcut(KEYUP, K_RIGHT, "right", self.camera.move.moveSpeed, (0, None))
        self.input.setShortcut(KEYUP, K_UP, "up", self.camera.move.moveSpeed, (None, 0))
        self.input.setShortcut(KEYUP, K_DOWN, "down", self.camera.move.moveSpeed, (None, 0))
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
        #self.map.save()

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def get(self, entityId):
        return self.entities.get(entityId)

    def toggleEditor(self):
        self.editorEnabled = not self.editorEnabled

    def process(self, controller, input):
        for entity in self.entities.values():
            if not entity.dead:
                if hasattr(entity, "move"):
                    entity.tick(entity.move(self.map, self.entities.values()))
                else:
                    entity.tick()

    def render(self, surface):
        self.map.draw(surface, self.camera)
        for entity in self.entities.values():
            entity.display(surface, self.camera)
        if self.editorEnabled:
            self.editor.draw(surface, self.camera)

    def tick(self, control, input):
        self.input(input)
        self.camera.tick()
        if self.editorEnabled:
            self.editor(input)
        self.process(control, input)
