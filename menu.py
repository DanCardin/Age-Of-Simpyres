import main
from display import *
from gconstants import *
from input import *
from pygame import Rect, Surface, MOUSEBUTTONDOWN


class Menu(object):
    def __init__(self, Pos, Showing):
        self.rect = Rect(Pos[0], Pos[1], screenSize[0] * res, screenSize[1] * res)
        self.items = {}
        self.input = Input(None, "MENU")
        self.tGroups = {}

    def append(self, Rect, Text, Actions, Colors=((255, 0, 0), (0, 0, 255), (0, 255, 0)), Image=False, Toggle=None):
        rect = (Rect[0] + self.rect.x, Rect[1] + self.rect.y, Rect[2], Rect[3])

        if len(Text) == 1:
            newItem = Text[0].lower()
        else:
            newItem = Text[1].lower()

        if isinstance(Actions, tuple):
            self.input.setShortcut(MOUSEBUTTONDOWN, newItem, newItem, Actions[0], Actions[1])
        else:
            self.input.setShortcut(MOUSEBUTTONDOWN, newItem, newItem, Actions)

        if Toggle is not None and self.tGroups.get(Toggle):
            self.tGroups[Toggle].append(newItem)
        else:
            self.tGroups[Toggle] = [newItem]

        self.items[newItem] = MenuItem(rect, newItem, Text[0], Actions, Colors[0], Colors[1], Colors[2], Image, Toggle)

    def animate(self, animation):
        """"""

    def select(self, key):
        return self.items[key.lower()]

    def tick(self, input):
        result = []
        for event, key in input:
            for item in self.items.values():
                itemClicked = item.tick(event, self.rect, key)
                if itemClicked:
                    result.append((MOUSEBUTTONDOWN, itemClicked))
                    if item.changed and item.toggle:
                        for i in self.tGroups[item.toggle]:
                            if item.ident != i:
                                self.items[i].toggledOn = False
        self.input(result)

    def draw(self, surface):
        for item in self.items.values():
            item.display(surface, item, "menu")


class MenuItem(Rect):
    def __init__(self, Rec, Ident, Text, Action, RColor, OColor, TColor, Image, Toggle):
        self.rect = Rect(Rec)
        self.ident = Ident
        self.images = [Surface((self.rect.w, self.rect.h)), Surface((self.rect.w, self.rect.h))]
        self.toggle = Toggle
        if self.toggle:
            self.toggledOn = False
            self.changed = False
        if isinstance(Action, list):
            self.action = Action
        else:
            self.action = [Action]
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
            return None
        if self.toggle and self.toggledOn:
            self.display.image = self.images[1]
        else:
            self.display.image = self.images[collide]
        if collide and input is MOUSEBUTTONDOWN:
            if self.toggle:
                self.toggledOn = True
                self.changed = True
            return self.ident
