import pygame
from pygame.locals import *

class Text():
    def __init__(self,x,y,text,size,color,font="assets/font.ttf") -> None:
        self.ttext = text
        self.color = color
        self.x = x
        self.y = y
        self.tfont = font
        self.size = size
        self.font = pygame.font.Font(self.tfont, self.size)
        self.text = self.font.render(self.ttext,False,self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (self.x,self.y)

    def update(self):
        self.font = pygame.font.Font(self.tfont, self.size)
        self.text = self.font.render(self.ttext,False,self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (self.x,self.y)

    def draw(self,surf,scroll=(0,0)):
        surf.blit(self.text, (self.text_rect.x - scroll[0],self.text_rect.y - scroll[1]))

class TypeBar:
    def __init__(self,x,y):
        self.type_def = ">"
        self.text = self.type_def
        self.type_text = Text(x,y,">",20,(200,200,200))

        self.input = ""

        self.limit = 30

    def events(self,event):
        if event.key == K_BACKSPACE: # backspace detect
            if len(self.text) > 1:
                self.text = self.text[:-1]

        elif event.key == K_RETURN: # enter detect
            self.input = self.text[1:]
            self.text = self.type_def

        else: # typing
            if len(self.text) < self.limit + 1:
                self.text += event.unicode

    def update(self):
        self.type_text.ttext = self.text
        self.type_text.update()

    def draw(self,surf):
        self.type_text.draw(surf)