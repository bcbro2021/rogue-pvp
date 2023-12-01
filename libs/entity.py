import pygame
from .assets import *

class Entity:
    def __init__(self,x=0,y=0):
        self.id = None
        self.scroll = [0,0]
        self.img = water_img
        self.rect = pygame.Rect(x,y,self.img.get_width(),self.img.get_height())

    def draw(self,dis,scroll):
        dis.blit(self.img,(self.rect.x - scroll[0],self.rect.y - scroll[1]))
