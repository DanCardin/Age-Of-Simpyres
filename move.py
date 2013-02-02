class Move(object):
    def __init__(self, Parent, Speed):
        self.topSpeed = Speed
        self.speed = [0, 0]
        self.parent = Parent
        if hasattr(Parent, "collision"):
            self._func = self.hasCollision
        else:
            self._func = self.noCollision

    def moveSpeed(self, dir):
        if not dir[0] == None:
            self.speed[0] = dir[0] * self.topSpeed[0]
        if not dir[1] == None:
            self.speed[1] = dir[1] * self.topSpeed[1]

    def noCollision(self):
        self.parent.rect.x += self.speed[0]
        self.parent.rect.y += self.speed[1]

    def hasCollision(self, Map, Objects):
        result = []
        collide = self.parent.collision

        self.parent.rect.x += self.speed[0]
        result.append(collide.Walls(Map, self.speed[0], 0))
        self.parent.rect.y += self.speed[1]
        result.append(collide.Walls(Map, 0, self.speed[1]))

        result.append(collide.Objects(Objects, 0, self.speed[1]))
        result.append(collide.Objects(Objects, self.speed[1], 0))
        return [x for x in result if x != None]

    def __call__(self, *args):
        return self._func(*args)
