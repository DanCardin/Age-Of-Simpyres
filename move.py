class Move(object):
    def __init__(self, Speed, Parent):
        self.topSpeed = Speed
        self.speed = [0, 0]
        self.parent = Parent
        self.pRect = self.parent.rect

    def moveSingleAxis(self, dx, dy):
        self.pRect.x += dx
        self.pRect.y += dy
        if hasattr(self.parent, "collision"):
            return self.parent.collision.collideWalls(dx, dy)

    def moveSingleAxissss(self, dx, dy):
        if hasattr(self.parent, "collision"):
            return self.parent.collision.collideEntities(dx, dy)

    def move(self):
        result = []
        if self.speed[0] != 0:
            r = [self.moveSingleAxis(self.speed[0], 0), self.moveSingleAxissss(self.speed[0], 0)]
            for i in r:
                if i != (None, None):
                    result.append(i)
        if self.speed[1] != 0:
            r = [self.moveSingleAxis(0, self.speed[1]), self.moveSingleAxissss(0, self.speed[1])]
            for i in r:
                if i != (None, None):
                    result.append(i)
        return result
