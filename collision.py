from gconstants import *


class Collision(object):
    def __init__(self, Parent, ColType):
        self.parent = Parent.rect
        self.colType = ColType

    def collDir(self, dx, dy, collideBox, t, retype):
        if t != 0:
            if dx > 0:
                if t == 1:
                    self.parent.right = collideBox.left
                return (retype, "right")
            elif dx < 0:
                if t == 1:
                    self.parent.left = collideBox.right
                return (retype, "left")
            elif dy > 0:
                if t == 1:
                    self.parent.bottom = collideBox.top
                return (retype, "bottom")
            elif dy < 0:
                if t == 1:
                    self.parent.top = collideBox.bottom
                return (retype, "top")
        return None

    def Walls(self, map, dx, dy):
        tx, ty = self.parent.x // res, self.parent.y // res
        for i, e in ((tx, ty), (tx + 1, ty), (tx, ty + 1), (tx + 1, ty + 1)):
            wallRect = map(i, e).rect
            if self.parent.colliderect(wallRect) and map(i, e).type == 1:
                return self.collDir(dx, dy, wallRect, map(i, e).type, map(i, e).type)
        return None

    def Objects(self, objects, dx, dy):
        for i in objects:
            if self.parent != i.rect:
                return self.collDir(dx, dy, i.rect, 1, self.colType)
        return None
