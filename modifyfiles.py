import sys
import os
import pygame


class ModifyFiles(object):
    def saveFile(self, input, file):
        fObj = open(os.path.join("assets", file), "w")
        fObj.write(input)
        fObj.close()

    def openFile(self, file):
        try:
            fObj = open(os.path.join("assets", file))
            s = fObj.read()
            fObj.close()
            return s
        except pygame.error(message):
            print("Cannot load file:", file)
            raise sys.exit()(message)

    def loadImage(self, file, colorkey=None):
        try:
            image = pygame.image.load(os.path.join("assets", file))
        except pygame.error(message):
            print("Cannot load image:", file)
            raise sys.exit()(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image
