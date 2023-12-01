import pygame
from .assets import *
from .settings import *

class Entity:
    def __init__(self,x=0,y=0):
        self.id = None
        self.scroll = [0,0]
        self.img = water_img
        self.rect = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())

    def draw(self,dis,scroll):
        dis.blit(self.img,(self.rect.x - scroll[0],self.rect.y - scroll[1]))

    def on_clicked(self,event, scroll):
        mouse_pos = pygame.mouse.get_pos()
        state = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint((mouse_pos[0]+scroll[0]),(mouse_pos[1]+scroll[1])):
                    print("lol")
