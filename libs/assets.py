import pygame
from .helper import *

# default
default_img = pygame.image.load("assets/basic_iso_tile.png")

# player imgs
player_idle = load_animation_frames("assets/player/idle",scale=2)

# tiles
# grass
grass_imgs = load_sprite_sheet("assets/world/grass_tilesheet.png",16,16,scale=2)

# water
water_img = pygame.Surface((32,32))
water_img.fill((95,205,228))

# bush
bush_img = load_image("assets/world/deco/bush.png",scale=3)