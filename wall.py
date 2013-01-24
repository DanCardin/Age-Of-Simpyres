from pygame import Rect


class Wall(Rect):
    def __init__(self, pos):
        Object.__init__(self, pos)
        self.type = pos[4]  # 0 = empty, 1 = solid
        self.tile = pos[5]