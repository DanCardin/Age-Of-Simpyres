from gconstants import *


class Collision(object):
    def __init__(self, Parent, ColType):
        self.parent = Parent.rect
        self.colType = ColType

    def collDir(self, dx, dy, collideBox, t, inst):
        if collideBox is not None and t != 0:
            if self.parent.colliderect(collideBox):
                if inst == "wall":
                    retype = t

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
        tx, ty = int(self.parent.x / res), int(self.parent.y / res)
        for h in [[tx, ty], [tx + 1, ty], [tx, ty + 1], [tx + 1, ty + 1]]:
            wallRect = map.wallDim(int(h[0]), int(h[1]))
            result = self.collDir(dx, dy, wallRect, map.getType(int(h[0]), int(h[1])), "wall")
            if result is not None:
                return result
        return None

    def Objects(self, objects, dx, dy):
        for i in objects:
            if self.parent != i.rect:
                return self.collDir(dx, dy, i.rect, 1, self.colType)
        return None
