import os

import pygame
from PIL import Image, ImageSequence


def load_image_from_gif(file_path, gif_name, images):
    image_gif = Image.open(file_path + gif_name + '.gif')
    frame_num = 0
    for frame in ImageSequence.Iterator(image_gif):
        frame_num += 1
        frame_name = gif_name + '_' + str(frame_num) + ".png"
        frame.save(file_path + frame_name, format='PNG', lossless=True)
        images.append(pygame.image.load(os.path.join(file_path, frame_name)).convert_alpha())

'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, colour, health):
        super().__init__()
        self.colour = colour
        self.health = health
        self.movement = [0,0]
        self.anim_index = 0

        self.is_moving = True
        self.facing_left = False
        self.facing_right = True
        self.is_turning = False
        self.is_dead = False

    def enem_movement(self, map):
        self.rect, enem_collisions = map.map_collision(self.rect, self.movement)
        self.movement = [0, 0]
        if enem_collisions['bottom']:
            self.y_momentum = 0
        if enem_collisions['left'] or enem_collisions['right']:
            self.x_momentum = 0
            self.is_turning = True
            if enem_collisions['left']:
                self.facing_right = True
                self.facing_left = False
            else:
                self.facing_left = True
                self.facing_right = False
        else:
            self.is_turning = False
            self.x_momentum = 1
        if self.facing_left:
            self.movement[0] -= self.x_momentum
        else:
            self.movement[0] += self.x_momentum
        self.x_momentum += 0.4
        if self.x_momentum > 1:
            self.x_momentum = 1
        self.movement[1] += self.y_momentum
        self.y_momentum += 0.4
        if self.y_momentum > 5:
            self.y_momentum = 5

    def is_hit(self):

    def death(self):

    def spawn(self):

    def aggravated(self):

    def animations(self):


    def draw(self, display, scroll):
        self.image = self.cur_anim[self.anim_index]
        display.blit(self.image, (self.rect.x - 2 - scroll[0], self.rect.y - 2 - scroll[1]))
'''


class AbstractPaintBlobEnemy(pygame.sprite.Sprite):
    def __init__(self, colour_index, loc):
        super().__init__()
        self.colour_states = {0: 'orange', 1: 'red', 2: 'yellow'}
        self.COLOUR_INDEX = colour_index
        self.colour = self.colour_states[self.COLOUR_INDEX]
        self.health = 4

        self.facing_left = False
        self.facing_right = True
        self.is_turning = False
        self.is_dead = False

        self.movement = loc
        self.y_momentum = 0
        self.x_momentum = 0

        self.anim_index = 0

        # all animations are facing left. facing right animations are the flipped versions of the animations
        self.move_anim = []
        self.move_right_anim = []
        self.turn_left_anim = []
        self.turn_right_anim = []
        self.death_left_anim = []
        self.death_right_anim = []

        self.set_colour()
        self.cur_anim = self.move_anim
        self.image = self.cur_anim[self.anim_index]
        self.anim_count_2 = 0
        self.rect = pygame.Rect(0,50,self.image.get_width()-4,self.image.get_height()-2)

    def draw(self, display, scroll):
        self.image = self.cur_anim[self.anim_index]
        display.blit(self.image, (self.rect.x - 2 - scroll[0], self.rect.y - 2 - scroll[1]))

    def animations(self):
        if self.is_turning:
            if self.facing_right:
                self.cur_anim = self.turn_left_anim
            else:
                self.cur_anim = self.turn_right_anim
        else:
            if self.facing_left:
                self.cur_anim = self.move_anim
            else:
                self.cur_anim = self.move_right_anim
        if self.is_dead:
            if self.facing_left:
                self.cur_anim = self.death_left_anim
            else:
                self.cur_anim = self.death_right_anim

    def change_frame(self, anim_count):
        if anim_count >= 5:
            if self.anim_count_2 > 1:
                if self.cur_anim == self.turn_left_anim and self.anim_index > 1:
                    self.cur_anim = self.move_anim
                elif (self.cur_anim == self.death_left_anim or self.cur_anim == self.death_right_anim) and self.anim_index > 1:
                    self.anim_index = 2
                elif self.anim_index >= len(self.cur_anim)-1:
                    self.anim_index = 0
                else:
                    self.anim_index += 1
                self.anim_count_2 = 0
            else:
                self.anim_count_2 += 1

    def enem_movement(self, map):
        self.rect, enem_collisions = map.map_collision(self.rect, self.movement)
        self.movement = [0, 0]
        if enem_collisions['bottom']:
            self.y_momentum = 0
        if (enem_collisions['left'] and self.facing_left) or enem_collisions['right']:
            self.x_momentum = 0
            self.is_turning = True
            if enem_collisions['left'] and self.facing_left:
                self.facing_right = True
                self.facing_left = False
            elif enem_collisions['right'] and self.facing_right:
                self.facing_left = True
                self.facing_right = False
        else:
            self.is_turning = False
            self.x_momentum = 1
        if self.facing_left:
            self.movement[0] -= self.x_momentum
        else:
            self.movement[0] += self.x_momentum
        self.x_momentum += 0.4
        if self.x_momentum > 1:
            self.x_momentum = 1
        self.movement[1] += self.y_momentum
        self.y_momentum += 0.4
        if self.y_momentum > 5:
            self.y_momentum = 5

    def update(self, anim_count, map, player_rect):
        if self.health > 0:
            self.enem_movement(map)
            self.is_dead = False
        else:
            self.is_dead = True
        self.change_frame(anim_count)
        self.animations()


    def set_colour(self):
        if self.COLOUR_INDEX == 0:
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_move/',
                                'paintblob_enemy_orange', self.move_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_move_right/',
                                'orange_move_right', self.move_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_turn/',
                                'orange_turn', self.turn_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_turn_right/',
                                'orange_turn_right', self.turn_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_death_left/',
                                'orange_death', self.death_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_orange/orange_death_right/',
                'orange_death', self.death_right_anim)
        elif self.COLOUR_INDEX == 1:
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_move_left/',
                                'paintblob_enemy_red', self.move_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_move_right/',
                                'paintblob_enemy_red', self.move_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_turn/',
                                'red_turn', self.turn_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_turn_right/',
                                'red_turn_right', self.turn_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_death_left/',
                'red_death', self.death_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_red/red_death_right/',
                'red_death', self.death_right_anim)
        elif self.COLOUR_INDEX == 2:
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_move_left/',
                                'paintblob_enemy_yellow', self.move_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_move_right/',
                                'paintblob_enemy_yellow', self.move_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_turn_left/',
                                'yellow_turn', self.turn_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_turn_right/',
                                'yellow_turn_right', self.turn_right_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_death_left/',
                'yellow_death', self.death_left_anim)
            load_image_from_gif(
                '../resources/textures/enemy_anim/paintblob_enem/paintblob_enem_move/paintblob_enem_yellow/yellow_death_right/',
                'yellow_death', self.death_right_anim)


class OrangePBEnem(AbstractPaintBlobEnemy):
    def __init__(self, loc):
        super().__init__(0, loc)


class RedPBEnem(AbstractPaintBlobEnemy):
    def __init__(self, loc):
        super().__init__(1, loc)


class YellowPBEnem(AbstractPaintBlobEnemy):
    def __init__(self, loc):
        super().__init__(2, loc)