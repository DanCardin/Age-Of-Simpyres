class Move(object):
    def __init__(self, Speed, Parent):
        self.topSpeed = Speed
        self.speed = [0, 0]
        self.parent = Parent
        self.pRect = self.parent.rect

    def moveSpeed(self, dir):
        if not dir[0] == None:
            self.speed[0] = dir[0] * self.topSpeed[0]
        if not dir[1] == None:
            self.speed[1] = dir[1] * self.topSpeed[1]

    def move(self):
        result = []
        self.pRect.x += self.speed[0]
        self.pRect.y += self.speed[1]
        if hasattr(self.parent, "collision"):
            collide = self.parent.collision
            result.append(collide.Walls(self.speed[0], 0))
            result.append(collide.Walls(0, self.speed[1]))
            result.append(collide.Objects(0, self.speed[1]))
            result.append(collide.Objects(0, self.speed[1]))
        return [x for x in result if x != None]
