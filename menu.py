import main
from display import *
from gconstants import *
from pygame import Rect, Surface, MOUSEBUTTONDOWN


class Menu(object):
    def __init__(self, Pos, Showing):
        self.rect = Rect(Pos[0], Pos[1], screenSize[0] * res, screenSize[1] * res)
        self.items = {}

    def append(self, Rect, Text, Actions, Colors=((255, 0, 0), (0, 0, 255), (0, 255, 0)), Image=False, Toggle=None):
        rect = (Rect[0] + self.rect.x, Rect[1] + self.rect.y, Rect[2], Rect[3])
        if len(Text) == 1:
            newItem = Text[0].lower()
        else:
            newItem = Text[1].lower()
        self.items[newItem] = MenuItem(Actions, rect, Colors[0], Colors[1], Text[0], Colors[2], Image, Toggle)

    def animate(self, animation):
        """"""

    def select(self, key):
        return self.items[key.lower()]

    def tick(self, input):
        for event, key in input:
            for item in self.items.values():
                item.tick(event, self.rect, key)
        for item in self.items.values():
            if item.changed:
                for key2, item2 in self.items.items():
                    if item != item2 and item.toggle == item2.toggle and item.changed == False:
                        item2.toggledOn = False

    def draw(self, surface):
        for item in self.items.values():
            item.display(surface, item, "menu")


class MenuItem(pygame.Rect):
    def __init__(self, Action, Rec, RColor, OColor, Text, TColor, Image, Toggle):
        self.rect = Rect(Rec)
        if isinstance(Action, list):
            self.action = Action
        else:
            self.action = [Action]
        self.images = [pygame.surface.Surface((self.rect.w, self.rect.h)), pygame.surface.Surface((self.rect.w, self.rect.h))]
        self.toggle = Toggle
        if self.toggle:
            self.toggledOn = False
            self.changed = False
        self.display = Display(self, self.images[0], self.images[0], False)

        self.rcolor = RColor
        self.ocolor = OColor
        self.tcolor = TColor
        self.text = Text
        self.image = Image
        self.update()

    def update(self, Rect=None, RColor=None, OColor=None, Text=None, TColor=None, Image=None):
        if Rect == None:
            Rect = self.rect
        if RColor == None:
            RColor = self.rcolor
        if OColor == None:
            OColor = self.ocolor
        if Text == None:
            Text = self.text
        if TColor == None:
            TColor = self.tcolor
        if Image == None:
            Image = self.image

        colors = [RColor, OColor]
        for i in range(len(colors)):
            self.images[i].fill(colors[i])
            if Text:
                if main.android:
                    text = pygame.surface.Surface((0, 0))
                else:
                    text = pygame.font.Font(None, 25).render(Text, 1, TColor)
                self.images[i].blit(text, ((self.images[i].get_width() / 2) - (text.get_width() / 2), (self.images[i].get_height() / 2) - (text.get_height() / 2)))
            if Image != False:
                self.images[i].blit(Image, (1, 1))

    def move(self, vect):
        self.rect.x += self.vect[0]
        self.rect.y += self.vect[1]

    def grow(self, dx, dy):
        self.rect.w += dx
        self.rect.h += dy

    def tick(self, input, menu, mPos):
        self.changed = False
        try:
            collide = self.rect.collidepoint(mPos)  # Fix this, stop the error rather than ignoring it
        except:
            return
        if self.toggle and self.toggledOn:
            self.display.image = self.images[1]
        else:
            self.display.image = self.images[collide]
        if input == MOUSEBUTTONDOWN:
            if collide:
                if self.toggle:
                    self.toggledOn = True
                    self.changed = True
                for i in self.action:
                    if hasattr(self.action[0], "__call__"):
                        if len(self.action) == 1:
                            self.action[0]()
                        else:
                            self.action[0](self.action[1])
                    else:
                        self.action[0] = self.action[1]
