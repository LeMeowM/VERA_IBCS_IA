import pygame
pygame.display.init()

floor_tile = pygame.image.load("floor.png").convert_alpha()
TILE_SIZE = 16

class Level():
    # load tile images here

    # pass map_file as a string that is the file path of the map

    def __init__(self, map_file):
        self.map_file = map_file
        self.map_text
        self.map_tiles = []
        self.map_collisions = []
        self.load_map()

    def load_map(self):
        f = open(self.map_file, "r")
        self.map_text = f.read()
        f.close()
        self.map_text = self.map_text.split('\n')
        for line in self.map_file:
            self.map_tiles.append(list(line))

    def draw_map(self, display):
        y = 0
        for line in self.map_tiles:
            x = 0
            for tile in line:
                if tile == '1':
                    display.blit(floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
                x += 1
            y += 1
