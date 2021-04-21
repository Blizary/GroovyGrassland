import pygame

class TEXT:

    def __init__(self, content, font, pos, color, screen):
        self.content = content
        self.font = font
        self.screen = screen
        self.pos = pos
        self.color = color
        self.texture = self.font.render(str(self.content), False, self.color)


    def ChangeAmount (self, amount):
        self.content += amount


    def UpdateText(self):
        self.texture = self.font.render(str(self.content), False, self.color)

    def ResetAmount(self):
        self.content = 0
        self.UpdateText()
