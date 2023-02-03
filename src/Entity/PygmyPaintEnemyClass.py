import pygame, sys, random
from PIL import Image, ImageSequence


def load_image_from_gif(file_path, gif_name, images):
    image_gif = Image.open(file_path + gif_name + '.gif')
    frame_num = 0
    for frame in ImageSequence.Iterator(image_gif):
        frame_num += 1
        frame_name = gif_name + '_' + str(frame_num) + ".png"
        frame.save(file_path + frame_name, format='PNG', lossless=True)
        images.append(pygame.image.load(file_path + frame_name).convert_alpha())


class AbstractPygmyPaintEnemy(pygame.sprite.Sprite):
    def __init__(self, colour_index, loc):
        super().__init__()
        self.colour_states = {0: 'orange', 1: 'red', 2: 'yellow'}
        self.COLOUR_INDEX = colour_index
        self.colour = self.colour_states[self.COLOUR_INDEX]
        self.health = 6

        self.facing_left = False
        self.facing_right = True
        self.is_angry = False
        self.is_attack = False
        self.is_turning = False
        self.is_dead = False
        self.is_idle = True
        self.is_avoid = False
        self.moving_right = False
        self.moving_left = False

        self.movement = loc
        self.y_momentum = 0
        self.x_momentum = 0

        self.anim_index = 0
        self.anger_timer = 0
        self.turn_count = 0
        self.x_count = 0
        self.y_count = 0
        self.attack_count = 0
        self.x_movement = ''
        self.y_movement = ''

        # idle anim refers to when the enemy is not angry
        self.idle_anim = []
        self.idle_right_anim = []
        # turn means turning from left to right
        self.idle_turn_anim = []
        # turn right means turning from right to left
        self.idle_turn_right_anim = []
        self.state_change_anim = []
        self.state_change_right_anim = []
        self.move_anim = []
        self.move_right_anim = []
        self.attack_anim = []
        self.attack_right_anim = []
        self.turn_left_anim = []
        self.turn_right_anim = []
        self.death_left_anim = []
        self.death_right_anim = []

        self.set_colour()
        self.cur_anim = self.idle_anim
        self.image = self.cur_anim[self.anim_index]
        self.rect = pygame.Rect(0,50,self.image.get_width(),self.image.get_height())
        self.detect_rect = pygame.Rect(0,50,self.image.get_width()+100,self.image.get_height()+50)
        self.detect_rect.center = self.rect.center

    def draw(self, display, scroll):
        self.image = self.cur_anim[self.anim_index]
        self.detect_rect.center = self.rect.center
        display.blit(self.image, (self.rect.x - 2 - scroll[0], self.rect.y - 2 - scroll[1]))

    def rand_turn(self):
        if self.turn_count >= 300:
            num = random.randint(1,2)
            if num == 1:
                self.is_turning = True
            self.turn_count = 0
        else:
            self.turn_count += 1

    def turn(self, player_rect):
        if player_rect.centerx < ((self.detect_rect.centerx - self.detect_rect.left)/2 + self.detect_rect.left) and self.facing_right:
            self.is_turning = True
            self.is_avoid = False
        elif player_rect.centerx > ((self.detect_rect.right - self.detect_rect.centerx)/2 + self.detect_rect.centerx) and self.facing_left:
            self.is_turning = True
            self.is_avoid = False
        else:
            self.is_avoid = True
            self.x_momentum = 2

    def avoid(self, player_rect):
        if player_rect.centery < ((self.detect_rect.centery - self.detect_rect.top)/2 + self.detect_rect.top):
            self.is_avoid = True
        elif player_rect.centery > ((self.detect_rect.bottom - self.detect_rect.centery)/2 + self.detect_rect.bottom):
            self.is_avoid = True

    def animations(self):
        if self.is_angry:
            if self.is_turning:
                if self.facing_right:
                    self.cur_anim = self.turn_right_anim
                else:
                    self.cur_anim = self.turn_left_anim
            else:
                if self.is_attack:
                    if self.facing_left:
                        self.cur_anim = self.attack_anim
                    else:
                        self.cur_anim = self.attack_right_anim
                else:
                    if self.facing_left:
                        self.cur_anim = self.move_anim
                    else:
                        self.cur_anim = self.move_right_anim
        elif self.is_angry:
            if self.is_turning:
                if self.facing_left:
                    self.cur_anim = self.idle_turn_anim
                else:
                    self.cur_anim = self.idle_turn_right_anim
            elif self.is_attack:
                if self.facing_left:
                    self.cur_anim = self.attack_anim
                else:
                    self.cur_anim = self.attack_right_anim
            else:
                if self.facing_left:
                    self.cur_anim = self.idle_anim
                else:
                    self.cur_anim = self.idle_right_anim
        if self.is_dead:
            if self.facing_left:
                self.cur_anim = self.idle_anim
            else:
                self.cur_anim = self.idle_right_anim

    def change_frame(self, anim_count):
        if anim_count >= 5:
            if self.is_turning and self.anim_index >= 6:
                if self.is_idle:
                    if self.cur_anim == self.idle_turn_anim:
                        self.cur_anim = self.idle_right_anim
                        self.facing_right = True
                        self.facing_left = False
                    elif self.cur_anim == self.idle_turn_right_anim:
                        self.cur_anim = self.idle_anim
                        self.facing_left = True
                        self.facing_right = False
                elif self.is_angry:
                    if self.cur_anim == self.turn_left_anim:
                        self.cur_anim = self.move_right_anim
                        self.facing_right = True
                        self.facing_left = False
                    elif self.cur_anim == self.turn_right_anim:
                        self.cur_anim = self.move_anim
                        self.facing_left = True
                        self.facing_right = False
                self.is_turning = False
            if self.is_attack and self.anim_index >= 5:
                if self.cur_anim == self.attack_anim:
                    self.anim_index = 0
                    self.cur_anim = self.move_anim
                elif self.cur_anim == self.attack_right_anim:
                    self.anim_index = 0
                    self.cur_anim = self.move_right_anim
                self.is_attack = False
            if self.anim_index >= len(self.cur_anim)-1:
                self.anim_index = 0
            else:
                self.anim_index += 1
            if self.is_dead:
                self.anim_index = 1

    def aggravate(self, player_rect):
        if pygame.Rect.colliderect(self.detect_rect, player_rect):
            self.is_angry = True
            self.is_idle = False
        else:
            if self.is_angry:
                if self.anger_timer >= 800:
                    self.is_angry = False
                    self.is_idle = True
                    self.anger_timer = 0
                else:
                    self.anger_timer += 1
            else:
                self.anger_timer = 0

    def attack(self):
        if self.attack_count >= 400:
            num = random.randint(1,2)
            if num == 1:
                self.is_attack = True
            else:
                self.is_attack = False
            self.attack_count = 0
        else:
            self.attack_count += 1

    def rand_y_movement(self):
        num = random.randint(1,3)
        if num == 1:
            return 2, 'top'
        elif num == 2:
            return 2, 'bottom'
        else:
            return 0, ''

    def rand_x_movement(self):
        num = random.randint(1,3)
        if num == 1:
            return 4, 'left'
        elif num == 2:
            return 4, 'right'
        else:
            return 0, ''

    def enem_movement(self, map):
        self.rect, enem_collisions = map.map_collision(self.rect, self.movement)
        self.movement = [0, 0]
        if self.is_idle:
            self.x_momentum, self.x_movement = self.rand_x_movement()
            self.x_count = 0
            self.y_momentum, self.y_movement = self.rand_y_movement()
            self.y_count = 0
            if self.x_count >= 300:
                if self.x_movement == 'left':
                    self.movement[0] -= self.x_momentum
                elif self.x_movement == 'right':
                    self.movement[0] += self.x_momentum
            else:
                self.x_count += 1
            if self.y_count >= 200:
                if self.y_movement == 'top':
                    self.movement[1] -= self.y_momentum
                elif self.y_movement == 'bottom':
                    self.movement[1] += self.y_momentum
            else:
                self.y_count += 1
            self.x_momentum -= 0.4
            if self.x_momentum <= 0:
                self.x_momentum = 0
        if (enem_collisions['left'] and self.facing_left) or (enem_collisions['right'] and self.facing_right):
            self.x_momentum = 0
            self.is_turning = True
            if enem_collisions['left'] and self.facing_left:
                self.facing_right = True
                self.facing_left = False
            elif enem_collisions['right'] and self.facing_right:
                self.facing_left = True
                self.facing_right = False
        elif (enem_collisions['left'] and self.facing_right) or (enem_collisions['right'] and self.facing_left):
            self.x_momentum = 2
        else:
            self.is_turning = False
        if self.is_idle:
            self.x_momentum = self.x_momentum/2
            self.y_momentum = self.y_momentum/2
        if self.facing_left:
            self.movement[0] -= self.x_momentum
        else:
            self.movement[0] += self.x_momentum
        if self.is_angry and self.is_avoid:
            if self.facing_left:
                self.movement[0] += self.x_momentum
                self.x_momentum -= 0.4
                if self.x_momentum <= 0:
                    self.x_momentum = 0
            else:
                self.movement[0] -= self.x_momentum
                self.x_momentum -= 0.4
                if self.x_momentum <= 0:
                    self.x_momentum = 2

    def update(self, anim_count, map, player_rect):
        if self.health > 0:
            self.is_dead = False
            self.enem_movement(map)
            self.aggravate(player_rect)
            if self.is_idle:
                self.rand_turn()
            else:
                self.turn(player_rect)
                self.avoid(player_rect)
                self.attack()
        else:
            self.is_dead = True
        self.change_frame(anim_count)
        self.animations()


    def set_colour(self):
        if self.COLOUR_INDEX == 0:
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/move_left/',
                                'move', self.move_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/move_right/',
                                'move', self.move_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/turn/',
                                'turn', self.turn_left_anim)
            load_image_from_gif('resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_orange/turn_right/',
                                'turn_right', self.turn_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/attack/',
                                'attack', self.attack_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/attack_right/',
                                'attack_right', self.attack_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/state_change_left/',
                                'state_change', self.state_change_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_orange/state_change_right/',
                                'state_change_right', self.state_change_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_orange/idle_left/',
                                'idle', self.idle_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_orange/idle_right/',
                                'idle', self.idle_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_orange/idle_turn/',
                                'idle_turn', self.idle_turn_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_orange/idle_turn_right/',
                                'idle_turn_right', self.idle_turn_right_anim)
        elif self.COLOUR_INDEX == 1:
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/move_left/',
                                'move', self.move_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/move_right/',
                                'move', self.move_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/turn/',
                                'turn', self.turn_left_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_red/turn_right/',
                                'turn_right', self.turn_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/attack/',
                                'attack', self.attack_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/attack_right/',
                                'attack_right', self.attack_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/state_change_left/',
                                'state_change', self.state_change_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_red/state_change_right/',
                                'state_change_right', self.state_change_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_red/idle_left/',
                                'idle', self.idle_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_red/idle_right/',
                                'idle', self.idle_right_anim)
            load_image_from_gif('resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_red/idle_turn/',
                                'idle_turn', self.idle_turn_anim)
            load_image_from_gif('resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_red/idle_turn_right/',
                                'idle_turn_right', self.idle_turn_right_anim)
        elif self.COLOUR_INDEX == 2:
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/move_left/',
                                'move', self.move_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/move_right/',
                                'move', self.move_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/turn/',
                                'turn', self.turn_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_yellow/idle_turn_right/',
                                'idle_turn_right', self.turn_right_anim)
            load_image_from_gif('../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/attack/',
                                'attack', self.attack_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/attack_right/',
                                'attack_right', self.attack_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/state_change_left/',
                                'state_change', self.state_change_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_move/pygmy_enem_yellow/state_change_right/',
                                'state_change_right', self.state_change_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_yellow/idle_left/',
                                'idle', self.idle_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_yellow/idle_right/',
                                'idle', self.idle_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_yellow/idle_turn/',
                                'idle_turn', self.idle_turn_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/pygmy_enem/pygmy_idle/pygmy_enem_yellow/idle_turn_right/',
                                'idle_turn_right', self.idle_turn_right_anim)


class OrangePygmyEnem(AbstractPygmyPaintEnemy):
    def __init__(self, loc):
        super().__init__(0, loc)


class RedPygmyEnem(AbstractPygmyPaintEnemy):
    def __init__(self, loc):
        super().__init__(1, loc)


class YellowPygmyEnem(AbstractPygmyPaintEnemy):
    def __init__(self, loc):
        super().__init__(2, loc)
