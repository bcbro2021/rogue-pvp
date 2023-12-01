import pygame, os, math, random
import noise
from .assets import *
from .tile import Tile
from .settings import *

def load_image(path,scale=1):
    img = pygame.image.load(f"{path}")
    scaled_img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
    return scaled_img


def load_animation_frames(path,scale=1):
    imgs = []
    files = os.listdir(path)
    for file in files:
        img = pygame.image.load(f"{path}/{file}")
        scaled_img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
        imgs.append(scaled_img)

    return imgs

def load_sprite_sheet(filename, sprite_width, sprite_height,scale=1):
    sheet = pygame.image.load(filename)
    sheet_width, sheet_height = sheet.get_size()

    sprites = []

    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            sprite = sheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))
            scaled_sprite = pygame.transform.scale(sprite,(sprite_width*scale,sprite_height*scale))
            sprites.append(scaled_sprite)

    return sprites

def generate_perlin_noise_map(width, height, scale):
    perlin_map = [[0] * height for _ in range(width)]

    for i in range(width):
        for j in range(height):
            perlin_map[i][j] = noise.pnoise2(i / scale,
                                             j / scale,
                                             octaves=6,
                                             persistence=0.5,
                                             lacunarity=2.0,
                                             repeatx=1024,
                                             repeaty=1024,
                                             base=1)

    return perlin_map

def create_island_map(width, height, scale):
    perlin_map = generate_perlin_noise_map(width, height, scale)

    island_map = [[0] * height for _ in range(width)]

    island_threshold = 0.2  # Adjust this threshold to control the size of the island

    for i in range(width):
        for j in range(height):
            island_map[i][j] = 1 if perlin_map[i][j] > island_threshold else 0

    # Apply a circular mask
    radius = min(width, height) // 2
    center_x, center_y = width // 2, height // 2

    for i in range(width):
        for j in range(height):
            distance = math.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            normalized_distance = distance / radius
            island_map[i][j] *= 1 if normalized_distance <= 1 else 0

    # check if water next to grass, if yes then change texture
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            if island_map[i][j] == 1 and island_map[i-1][j] == 0: # left side
                island_map[i][j] = 2
            if island_map[i][j] == 1 and island_map[i+1][j] == 0: # right side
                island_map[i][j] = 3

            if island_map[i][j] == 1 and island_map[i][j+1] == 0: # bottom side
                island_map[i][j] = 4
            if island_map[i][j] == 1 and island_map[i][j-1] == 0: # top side
                island_map[i][j] = 5

            # corners
            if island_map[i][j] > 0 and island_map[i-1][j] == 0 and island_map[i][j-1] == 0: # top left
                island_map[i][j] = 6
            if island_map[i][j] > 0 and island_map[i+1][j] == 0 and island_map[i][j-1] == 0: # top right
                island_map[i][j] = 7
            if island_map[i][j] > 0 and island_map[i-1][j] == 0 and island_map[i][j+1] == 0: # bottom left
                island_map[i][j] = 8
            if island_map[i][j] > 0 and island_map[i+1][j] == 0 and island_map[i][j+1] == 0: # bottom right
                island_map[i][j] = 9

            # triple side corners
            if island_map[i][j] > 0 and island_map[i][j-1] == 0 and island_map[i][j+1] == 0: # middle
                island_map[i][j] = 12
            if island_map[i][j] > 0 and island_map[i+1][j] == 0 and island_map[i-1][j] == 0: # middle vertical
                island_map[i][j] = 15
            if island_map[i][j] > 0 and island_map[i-1][j] == 0 and island_map[i][j-1] == 0 and island_map[i][j+1] == 0: # left
                island_map[i][j] = 10
            if island_map[i][j] > 0 and island_map[i+1][j] == 0 and island_map[i][j-1] == 0 and island_map[i][j+1] == 0: # right
                island_map[i][j] = 11
            if island_map[i][j] > 0 and island_map[i][j-1] == 0 and island_map[i-1][j] == 0 and island_map[i+1][j] == 0: # top
                island_map[i][j] = 13
            if island_map[i][j] > 0 and island_map[i][j+1] == 0 and island_map[i-1][j] == 0 and island_map[i+1][j] == 0: # bottom
                island_map[i][j] = 14

            # all sides
            if island_map[i][j] > 0 and (
                    island_map[i-1][j] == 0 and island_map[i+1][j] == 0 and
                    island_map[i][j-1] == 0 and island_map[i][j+1] == 0):
                island_map[i][j] = 16

    return island_map

def load_map_tiles(_map,grass_imgs,water_img):
    tiles = []
    water = []
    for y in range(MAP_WIDTH - 10):
        for x in range(MAP_HEIGHT - 30):

            # sides and water
            if _map[x][y] == 1:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[4]))
            if _map[x][y] == 0:
                water.append(Tile(x*TILE_SIZE,y*TILE_SIZE,water_img))
            if _map[x][y] == 2:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[3]))
            if _map[x][y] == 3:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[5]))
            if _map[x][y] == 4:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[7]))
            if _map[x][y] == 5:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[1]))

            # corners
            if _map[x][y] == 6:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[0]))
            if _map[x][y] == 7:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[2]))
            if _map[x][y] == 8:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[6]))
            if _map[x][y] == 9:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[8]))

            # triple corners
            if _map[x][y] == 10:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[18]))
            if _map[x][y] == 11:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[20]))
            if _map[x][y] == 12:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[19]))
            if _map[x][y] == 13:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[22]))
            if _map[x][y] == 14:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[28]))
            if _map[x][y] == 15:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[25]))

            # all sides
            if _map[x][y] == 16:
                tiles.append(Tile(x*TILE_SIZE,y*TILE_SIZE,grass_imgs[21]))
            
    return water, tiles

def generate_deco(deco_data,img):
    tiles = []
    for deco in deco_data:
        tiles.append(Tile(deco[0],deco[1],img))
    return tiles

def create_game_map_from_text(text_map):
    game_map = []
    map_rows = text_map.split(".")
    for row in map_rows:
        map_chars = row.split(",")
        row = []
        for i in range(len(map_chars)-1):
            row.append(int(map_chars[i]))
        game_map.append(row)
    return game_map