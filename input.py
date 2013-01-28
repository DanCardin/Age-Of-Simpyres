from modifyfiles import *
import pygame


class Input(object):
    def __init__(self, Settings, Keyword):
        self.inputt = {}
        self.keyword = ("-" + Keyword + "-", "-/" + Keyword + "-")
        self.settings = Settings
        self.shortcuts = ({}, {})

        self.k = False#self.getKeys(",")
        if self.k:
            self.inputt = self.k

    def setShortcut(self, event, updown, key, action, arg=False):
        if not self.k:
            if not self.inputt.get(event):
                self.inputt[event] = key
        self.shortcuts[updown == "down"][key] = (action, arg)

    def useShortcut(self, updown, key):
        get = self.shortcuts[updown].get(key)
        if get:
            if hasattr(get[0], "__call__"):
                if get[1]:
                    get[0](get[1])
                else:
                    get[0]()
            else:
                get[0] = get[1]

    def checkInput(self, inputs):
        if len(inputs) != 0:
            for inputy in inputs:
                cInput = self.get(inputy)
                if cInput != - 1:
                    self.useShortcut(cInput[0], cInput[1])

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
        k = sorted(self.inputt.items(), key=lambda v: (v[1], v[0]))
        s = self.keyword[0] + "".join([x[1] + ":" + str(x[0]) + "," for x in k]) + self.keyword[1]
        f = ModifyFiles().openFile(self.settings)
        p = f.find(self.keyword[0], 0)
        ep = f.find(self.keyword[1], 0)
        if p != -1 and ep != -1:
            f = f[:p] + s + f[ep + len(self.keyword[1]):]
        else:
            f = s + f
        ModifyFiles().saveFile(f, self.settings)

    def get(self, inputy):
        t = self.inputt.get(inputy[1])
        if t:
            return (inputy[0] == pygame.KEYDOWN, t)
        return -1
