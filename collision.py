from gconstants import *


class Collision(object):
    def __init__(self, Parent, Level, ColType):
        self.parent = Parent
        self.pRect = self.parent.rect
        self.level = Level
        self.colType = ColType

    def collDir(self, dx, dy, collideBox, t, inst=0):
        result = None
        if collideBox != None and t != 0:
            if self.pRect.colliderect(collideBox):
                if inst != 0:
                    retype = inst
                else:
                    retype = t
                if dx > 0:
                    if t == 1:
                        self.pRect.right = collideBox.left
                    result = (retype, "right")
                if dx < 0:
                    if t == 1:
                        self.pRect.left = collideBox.right
                    result = (retype, "left")
                if dy > 0:
                    if t == 1:
                        self.pRect.bottom = collideBox.top
                    result = (retype, "bottom")
                if dy < 0:
                    if t == 1:
                        self.pRect.top = collideBox.bottom
                    result = (retype, "top")
        return result

    def collideWalls(self, dx, dy):
        tx, ty = int(self.pRect.x / res), int(self.pRect.y / res)
        rects = [[tx, ty], [tx + 1, ty], [tx, ty + 1], [tx + 1, ty + 1]]

        result = (None, None)
        for h in rects:
            ww = self.level.map.wallDim(int(h[0]), int(h[1]))
            temp = self.collDir(dx, dy, ww, self.level.map.getType(int(h[0]), int(h[1])))
            if temp != None:
                result = temp
        return result

    def collideEntities(self, dx, dy):
        for i in range(self.level.entityId):
            obj = self.level.get(i)
            if self.parent != obj:
                #if self.parent.inertia < obj.inertia:
                temp = self.collDir(dx, dy, obj.rect, 1, self.colType)
                if temp != None:
                    return temp
        return (None, None)
