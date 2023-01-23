import pygame

class LevelManager:
    def __init__(self, level_map):
        # level_map is a Level object
        self.level_map = level_map
        self.level_map.load_map()
        self.enemies = {}
        self.items = []
        self.map_objects = []
        self.room_index = 0

    def add_enem(self, enemy):
        self.enemies.update({enemy: enemy.is_dead})

    def draw(self, display, scroll):
        for enemy in self.enemies:
            enemy.draw(display, scroll)

    def set_room_index(self, room_index):
        self.room_index = room_index

    def update(self, anim_count):
        for enemy in self.enemies:
            enemy.update(anim_count, self.level_map)
            self.enemies[enemy] = enemy.is_dead


pygame.display.set_mode()
floor_tile = pygame.image.load("floor.png").convert_alpha()
black_tile = pygame.image.load("black_tile.png").convert_alpha()
TILE_SIZE = 16


class Level:
    # pass map_file as a string that is the file path of the map
    def __init__(self, map):
        self.map_file = map
        self.map_text = []
        self.map_tiles = []
        self.map_rects = []
        self.map_colliders = []

    def load_map(self):
        f = open(self.map_file, "r")
        self.map_text = f.read()
        f.close()
        self.map_text = self.map_text.split('\n')
        for line in self.map_text:
            self.map_tiles.append(list(line))

    def draw_map(self, display_surface, scroll):
        self.map_rects = []
        y = 0
        for line in self.map_tiles:
            x = 0
            for tile in line:
                if tile == "1":
                    display_surface.blit(floor_tile, (x * TILE_SIZE - 50 - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == "x":
                    display_surface.blit(black_tile, (x * TILE_SIZE - 50 - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile != "0":
                    self.map_rects.append(pygame.Rect((x * TILE_SIZE - 50, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
                x += 1
            y += 1

    def test_map_collision(self, rect):
        self.map_colliders = []
        for tile in self.map_rects:
            if pygame.Rect.colliderect(rect, tile):
                self.map_colliders.append(tile)

    def map_collision(self, rect, movement):
        collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        rect.x += movement[0]
        self.test_map_collision(rect)
        for tile in self.map_colliders:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        self.test_map_collision(rect)
        for tile in self.map_colliders:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types