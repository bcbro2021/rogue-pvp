import pygame
from pygame.locals import *
from libs.game import *

pygame.init()

game = Game()

while True:
    for event in pygame.event.get():
        game.events(event)

    # update
    game.update()

    # rendering
    game.draw()

    pygame.display.update()
    game.clock.tick(MAX_FPS)