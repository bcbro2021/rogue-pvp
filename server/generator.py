import noise, math, random
from settings import *

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

def create_text_map(game_map):
    text_map = ""
    for i in range(len(game_map)):
        text_row = ""
        for j in range(len(game_map[i])):
            text_row = text_row + str(game_map[i][j]) + ","
        text_map = text_map + text_row + "."
    
    return text_map

def generate_deco(_map,rarity=5):
    tiles = []
    for y in range(MAP_WIDTH - 10):
        for x in range(MAP_HEIGHT - 30):
            if _map[x][y] == 1:
                chance = random.randint(0,rarity)
                if chance == 1:
                    tiles.append([x*TILE_SIZE,y*TILE_SIZE])
    
    return tiles