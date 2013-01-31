from modifyfiles import *
import pygame


class Input(object):
    def __init__(self, Settings, Keyword):
        self.keys = {}
        self.keyword = ("-" + Keyword + "-", "-/" + Keyword + "-")
        self.settings = Settings
        self.shortcuts = {}

        self.k = False  # self.getKeys(",")
        if self.k:
            self.keys = self.k

    def setShortcut(self, event, key, label, action, arg=False):
        if not self.k:
            if not self.keys.get(key):
                self.keys[key] = label
        if not self.shortcuts.get(event):
            self.shortcuts[event] = {}
        self.shortcuts[event][label] = (action, arg)

    def useShortcut(self, validInput):
        #print(self.shortcuts)
        event, key = validInput
        print (event, key)
        action, argument = event[key]
        if action:
            if hasattr(action, "__call__"):
                if argument:
                    action(argument)
                else:
                    action()
            else:
                action = argument

    def get(self, action, key):
        print(action, key)
        validShortcut = self.shortcuts.get(action)
        validValue = self.keys.get(key)
        if validShortcut and validValue:
            return (validShortcut, validValue)
        return None

    def checkInput(self, inputs):
        for action, key in inputs:
            validInput = self.get(action, key)
            if validInput:
                self.useShortcut(validInput)

    def getKeys(self, delim):
        keys = {}
        s = ModifyFiles().openFile(self.settings)
        p = s.find(self.keyword[0], 0)
        c = s.find(self.keyword[1], 0)
        if p == -1 or c == -1:
            return False
        else:
            s = s[p + len(self.keyword[0]):c]
            p = 0
            c = 0
            while True:
                c = s.find(delim, p)
                if c == -1:
                    break
                t = s[p:c]
                r = t.find(":")
                keys[int(t[r + 1:])] = t[:r]
                p = c + 1
            return keys

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
