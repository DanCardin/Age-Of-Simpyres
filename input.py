import re
from modifyfiles import *


class Input(object):
    def __init__(self, Settings, Keyword):
        self.keys = {}
        self.keyword = ("-" + Keyword + "-", "-/" + Keyword + "-")
        self.settings = Settings
        self.shortcuts = {}

        if self.settings:
            self.k = False  # self.getKeys(",")
        else:
            self.k = False

    def setShortcut(self, event, key, label, action, arg=None):
        if not self.k:
            if not self.keys.get(key):
                self.keys[key] = label
        if not self.shortcuts.get(event):
            self.shortcuts[event] = {}
        self.shortcuts[event][label] = (action, arg)

    def useShortcut(self, event, key):
        action, argument = event[key]
        if action:
            if hasattr(action, "__call__"):
                if argument is not None:
                    action(argument)
                else:
                    action()
            else:
                action = argument

    def __call__(self, inputs):
        for event, key in inputs:
            validEvent = self.shortcuts.get(event)
            validShortcut = self.keys.get(key)
            if validEvent and validShortcut:
                if validEvent.get(validShortcut):
                    self.useShortcut(validEvent, validShortcut)

    def getKeys(self, delim):
        catagory = re.search(self.keyword[0] + "(.*?)" + self.keyword[1], ModifyFiles().openFile(self.settings))
        if catagory:
            for i in re.finditer("((?:[a-z][a-z]+)):(\d+),", catagory.group(1)):
                self.keys[i.group(1)] = int(i.group(2))
            return True
        else:
            return False

    def setKeys(self):
        k = sorted(self.keys.items(), key=lambda v: (v[1], v[0]))
        s = self.keyword[0] + "".join([x[1] + ":" + str(x[0]) + "," for x in k]) + self.keyword[1]
        f = ModifyFiles().openFile(self.settings)
        p = f.find(self.keyword[0], 0)
        ep = f.find(self.keyword[1], 0)
        if p != -1 and ep != -1:
            f = f[:p] + s + f[ep + len(self.keyword[1]):]
        else:
            f = s + f
        ModifyFiles().saveFile(f, self.settings)
