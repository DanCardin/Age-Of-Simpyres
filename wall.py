from pygame import Rect


class Wall(object):
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], pos[2], pos[3])
        self.type = pos[4]  # 0 = empty, 1 = solid
        self.tile = pos[5]
