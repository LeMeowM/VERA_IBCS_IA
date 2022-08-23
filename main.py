import pygame, sys
from PlayerClass import Player

clock = pygame.time.Clock()
pygame.display.set_caption('Colour!')

pygame.init()

WINDOW_SIZE = (1280, 640)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((640, 320))

# player init
player = Player()

# load tile images here

floor_tile = pygame.image.load("floor.png").convert_alpha()
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

    def draw_map(self, display_surface):
        self.map_rects = []
        y = 0
        for line in self.map_tiles:
            x = 0
            for tile in line:
                if tile == "1":
                    display_surface.blit(floor_tile, (x * TILE_SIZE, y * TILE_SIZE))
                if tile != "0":
                    self.map_rects.append(pygame.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
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
                movement[1] = 0
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                movement[1] = 2
                collision_types['top'] = True
        return rect, collision_types


# levels
level_one = Level('map.txt')
level_one.load_map()

player.becomes_colourful()

# run game
while True:
    display.fill((146, 244, 255))

    level_one.draw_map(display)
    player.player_movement = [0,0]
    player.movement()
    player.change_colour()

    player.rect, collisions = level_one.map_collision(player.rect, player.player_movement)
    if collisions['bottom']:
        player.player_y_momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1
    if collisions['top']:
        player.player_y_momentum = 2

    display.blit(player.image, (player.rect.x, player.rect.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and player.is_colourful:
                player.is_changing_colour = True
            if event.key == pygame.K_z:
                if player.air_timer < 6:
                    player.player_y_momentum = -7
                    player.is_jumping = True
            if not player.is_changing_colour:
                if event.key == pygame.K_RIGHT:
                    player.moving_right = True
                if event.key == pygame.K_LEFT:
                    player.moving_left = True
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player.colour_index += 1
                    if player.colour_index > 2:
                        player.colour_index = 0
                elif keys[pygame.K_RIGHT]:
                    player.colour_index -= 1
                    if player.colour_index < 0:
                        player.colour_index = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            if event.key == pygame.K_z:
                player.is_jumping = False
            if event.key == pygame.K_LSHIFT and player.is_colourful:
                player.is_changing_colour = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
