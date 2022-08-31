import pygame
from sys import exit
from PIL import Image, ImageSequence


pygame.init()


def load_image_from_gif(file_path, gif_name, images):
    image_gif = Image.open(file_path + gif_name + '.gif')
    frame_num = 0
    for frame in ImageSequence.Iterator(image_gif):
        frame_num += 1
        frame_name = gif_name + '_' + str(frame_num) + ".png"
        frame.save(file_path + frame_name, format='PNG', lossless=True)
        images.append(pygame.image.load(file_path + frame_name).convert_alpha())


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # colour states
        self.is_colourful = False
        self.is_changing_colour = False
        default_state = pygame.image.load('player_default.png').convert_alpha()
        blue_state = pygame.image.load('player_blue.png').convert_alpha()
        green_state = pygame.image.load('player_green.png').convert_alpha()
        purple_state = pygame.image.load('player_purple.png').convert_alpha()
        self.player_colours = {'blue': False, 'green': False, 'purple': False}
        # self.player_colours = [blue_state, green_state, purple_state, default_state]
        self.colour_index = 3
        self.damage = 0
        self.idle_count = 0

        self.default_anim_frames = []
        self.default_idle_left_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_idle_left/', 'player_default_idle_left',
                            self.default_idle_left_frames)
        self.default_idle_right_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_idle_right/', 'player_default_idle_right',
                            self.default_idle_right_frames)
        self.default_moving_right_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_moving_right/', 'player_default_moving_right',
                            self.default_moving_right_frames)
        self.default_moving_left_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_moving_left/', 'player_default_moving_left',
                            self.default_moving_left_frames)
        self.default_jumping_left_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_jumping_left/', 'player_default_jumping_left',
                            self.default_jumping_left_frames)
        self.default_falling_left_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_falling_left/', 'player_default_falling_left', self.default_falling_left_frames)
        self.default_jumping_right_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_jumping_right/',
                            'player_default_jumping_right',
                            self.default_jumping_right_frames)
        self.default_falling_right_frames = []
        load_image_from_gif('player_anim/player_default_anim/player_default_falling_right/',
                            'player_default_falling_right', self.default_falling_right_frames)
        self.default_attacking_frames = []
        self.default_damaged_frames = []

        self.blue_anim_frames = []
        self.blue_idle_left_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_idle_left/', 'player_blue_idle_left',
                            self.blue_idle_left_frames)
        self.blue_idle_right_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_idle_right/', 'player_blue_idle_right',
                            self.blue_idle_right_frames)
        self.blue_moving_right_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_moving_right/', 'player_blue_moving_right',
                            self.blue_moving_right_frames)
        self.blue_moving_left_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_moving_left/', 'player_blue_moving_left',
                            self.blue_moving_left_frames)
        self.blue_jumping_left_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_jumping_left/', 'player_blue_jumping_left',
                            self.blue_jumping_left_frames)
        self.blue_falling_left_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_falling_left/',
                            'player_blue_falling_left', self.blue_falling_left_frames)
        self.blue_jumping_right_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_jumping_right/', 'player_blue_jumping_right',
                            self.blue_jumping_right_frames)
        self.blue_falling_right_frames = []
        load_image_from_gif('player_anim/player_blue_anim/player_blue_falling_right/',
                            'player_blue_falling_right', self.blue_falling_right_frames)
        self.blue_attacking_frames = []
        self.blue_damaged_frames = []

        self.green_anim_frames = []
        self.green_idle_left_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_idle_left/', 'player_green_idle_left',
                            self.green_idle_left_frames)
        self.green_idle_right_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_idle_right/', 'player_green_idle_right',
                            self.green_idle_right_frames)
        self.green_moving_right_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_moving_right/', 'player_green_moving_right',
                            self.green_moving_right_frames)
        self.green_moving_left_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_moving_left/', 'player_green_moving_left',
                            self.green_moving_left_frames)
        self.green_jumping_left_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_jumping_left/', 'player_green_jumping_left',
                            self.green_jumping_left_frames)
        self.green_falling_left_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_falling_left/',
                            'player_green_falling_left', self.green_falling_left_frames)
        self.green_jumping_right_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_jumping_right/', 'player_green_jumping_right',
                            self.green_jumping_right_frames)
        self.green_falling_right_frames = []
        load_image_from_gif('player_anim/player_green_anim/player_green_falling_right/',
                            'player_green_falling_right', self.green_falling_right_frames)
        self.green_attacking_frames = []
        self.green_damaged_frames = []

        self.purple_anim_frames = []
        self.purple_idle_left_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_idle_left/', 'player_purple_idle_left',
                            self.purple_idle_left_frames)
        self.purple_idle_right_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_idle_right/', 'player_purple_idle_right',
                            self.purple_idle_right_frames)
        self.purple_moving_right_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_moving_right/', 'player_purple_moving_right',
                            self.purple_moving_right_frames)
        self.purple_moving_left_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_moving_left/', 'player_purple_moving_left',
                            self.purple_moving_left_frames)
        self.purple_jumping_left_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_jumping_left/', 'player_purple_jumping_left',
                            self.purple_jumping_left_frames)
        self.purple_falling_left_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_falling_left/',
                            'player_purple_falling_left', self.purple_falling_left_frames)
        self.purple_jumping_right_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_jumping_right/', 'player_purple_jumping_right',
                            self.purple_jumping_right_frames)
        self.purple_falling_right_frames = []
        load_image_from_gif('player_anim/player_purple_anim/player_purple_falling_right/',
                            'player_purple_falling_right', self.purple_falling_right_frames)
        self.purple_attacking_frames = []
        self.purple_damaged_frames = []

        self.cur_anim = self.default_idle_left_frames
        self.anim_index = 0
        self.image = self.cur_anim[self.anim_index]

        # player location and movement variables
        self.facing_left = False
        self.facing_right = False
        self.is_idle = False
        self.moving_right = False
        self.moving_left = False
        self.is_jumping = False
        self.is_falling = False
        self.player_y_momentum = 0
        self.player_x_momentum = 0
        self.player_movement = [0, 0]
        self.health = 10
        self.air_timer = 0
        self.rect = pygame.Rect(50, 0, default_state.get_width()-6, default_state.get_height())

    def draw(self, screen, scroll):
        self.image = self.cur_anim[self.anim_index]
        screen.blit(self.image, (self.rect.x - 3 - scroll[0], self.rect.y - scroll[1]))

    """
    # takes user input from keyboard
    def player_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not event.key == pygame.K_LSHIFT:
                    if event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                else:
                    self.change_colour()
                if pygame.key == pygame.K_z:
                    self.player_y_momentum = -3
                    self.is_jumping = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                if event.key == pygame.K_UP:
                    self.is_jumping = False
    
    """

    def animations(self):
        initial_anim = self.cur_anim
        if self.is_colourful:
            if self.player_colours['blue']:
                self.blue_anim()
            elif self.player_colours['green']:
                self.green_anim()
            else:
                self.purple_anim()
        else:
            self.default_anim()
        if initial_anim != self.cur_anim:
            self.anim_index = 0

    def default_anim(self):
        initial_anim = self.cur_anim
        if self.is_idle:
            if self.facing_left:
                self.cur_anim = self.default_idle_left_frames
            else:
                self.cur_anim = self.default_idle_right_frames
        elif self.moving_left or self.moving_right:
            if self.facing_left:
                self.cur_anim = self.default_moving_left_frames
            else:
                self.cur_anim = self.default_moving_right_frames
        if self.is_jumping:
            if self.facing_left:
                self.cur_anim = self.default_jumping_left_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
            else:
                self.cur_anim = self.default_jumping_right_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
        elif self.is_falling:
            if initial_anim == self.default_jumping_left_frames:
                self.anim_index = 3
            elif self.anim_index == 3:
                if initial_anim == self.default_falling_left_frames or initial_anim == self.default_falling_right_frames:
                    self.anim_index = 3
            else:
                if self.facing_left:
                    self.cur_anim = self.default_falling_left_frames
                else:
                    self.cur_anim = self.default_falling_right_frames
            if initial_anim == self.default_falling_left_frames or initial_anim == self.default_falling_right_frames:
                if self.anim_index >= 1:
                    self.anim_index = 1
        elif not self.is_falling and (initial_anim == self.default_falling_left_frames or initial_anim == self.default_falling_right_frames):
            if initial_anim == self.default_falling_left_frames or initial_anim == self.default_falling_right_frames:
                if self.anim_index < 4:
                    if self.facing_left:
                        self.cur_anim = self.default_falling_left_frames
                    else:
                        self.cur_anim = self.default_falling_right_frames
            else:
                self.is_idle = True
                if self.facing_left:
                    self.cur_anim = self.default_idle_left_frames
                else:
                    self.cur_anim = self.default_idle_right_frames

    def blue_anim(self):
        initial_anim = self.cur_anim
        if self.is_idle:
            if self.facing_left:
                self.cur_anim = self.blue_idle_left_frames
            else:
                self.cur_anim = self.blue_idle_right_frames
        elif self.moving_left or self.moving_right:
            if self.facing_left:
                self.cur_anim = self.blue_moving_left_frames
            else:
                self.cur_anim = self.blue_moving_right_frames
        if self.is_jumping:
            if self.facing_left:
                self.cur_anim = self.blue_jumping_left_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
            else:
                self.cur_anim = self.blue_jumping_right_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
        elif self.is_falling:
            if initial_anim == self.blue_jumping_left_frames:
                self.anim_index = 3
            elif self.anim_index == 3:
                if initial_anim == self.blue_falling_left_frames or initial_anim == self.blue_falling_right_frames:
                    self.anim_index = 3
            else:
                if self.facing_left:
                    self.cur_anim = self.blue_falling_left_frames
                else:
                    self.cur_anim = self.blue_falling_right_frames
            if initial_anim == self.blue_falling_left_frames or initial_anim == self.blue_falling_right_frames:
                if self.anim_index >= 1:
                    self.anim_index = 1
        elif not self.is_falling and (initial_anim == self.blue_falling_left_frames or initial_anim == self.blue_falling_right_frames):
            if initial_anim == self.blue_falling_left_frames or initial_anim == self.blue_falling_right_frames:
                if self.anim_index < 4:
                    if self.facing_left:
                        self.cur_anim = self.blue_falling_left_frames
                    else:
                        self.cur_anim = self.blue_falling_right_frames
            else:
                self.is_idle = True
                if self.facing_left:
                    self.cur_anim = self.blue_idle_left_frames
                else:
                    self.cur_anim = self.blue_idle_right_frames

    def green_anim(self):
        initial_anim = self.cur_anim
        if self.is_idle:
            if self.facing_left:
                self.cur_anim = self.green_idle_left_frames
            else:
                self.cur_anim = self.green_idle_right_frames
        elif self.moving_left or self.moving_right:
            if self.facing_left:
                self.cur_anim = self.green_moving_left_frames
            else:
                self.cur_anim = self.green_moving_right_frames
        if self.is_jumping:
            if self.facing_left:
                self.cur_anim = self.green_jumping_left_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
            else:
                self.cur_anim = self.green_jumping_right_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
        elif self.is_falling:
            if initial_anim == self.green_jumping_left_frames:
                self.anim_index = 3
            elif self.anim_index == 3:
                if initial_anim == self.green_falling_left_frames or initial_anim == self.green_falling_right_frames:
                    self.anim_index = 3
            else:
                if self.facing_left:
                    self.cur_anim = self.green_falling_left_frames
                else:
                    self.cur_anim = self.green_falling_right_frames
            if initial_anim == self.green_falling_left_frames or initial_anim == self.green_falling_right_frames:
                if self.anim_index >= 1:
                    self.anim_index = 1
        elif not self.is_falling and (initial_anim == self.green_falling_left_frames or initial_anim == self.green_falling_right_frames):
            if initial_anim == self.green_falling_left_frames or initial_anim == self.green_falling_right_frames:
                if self.anim_index < 4:
                    if self.facing_left:
                        self.cur_anim = self.green_falling_left_frames
                    else:
                        self.cur_anim = self.green_falling_right_frames
            else:
                self.is_idle = True
                if self.facing_left:
                    self.cur_anim = self.green_idle_left_frames
                else:
                    self.cur_anim = self.green_idle_right_frames

    def purple_anim(self):
        initial_anim = self.cur_anim
        if self.is_idle:
            if self.facing_left:
                self.cur_anim = self.purple_idle_left_frames
            else:
                self.cur_anim = self.purple_idle_right_frames
        elif self.moving_left or self.moving_right:
            if self.moving_left:
                self.cur_anim = self.purple_moving_left_frames
            else:
                self.cur_anim = self.purple_moving_right_frames
        if self.is_jumping:
            if self.facing_left:
                self.cur_anim = self.purple_jumping_left_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
            else:
                self.cur_anim = self.purple_jumping_right_frames
                if self.anim_index >= 2:
                    self.anim_index = 2
        elif self.is_falling:
            if initial_anim == self.purple_jumping_left_frames:
                self.anim_index = 3
            elif self.anim_index == 3:
                if initial_anim == self.purple_falling_left_frames or initial_anim == self.purple_falling_right_frames:
                    self.anim_index = 3
            else:
                if self.facing_left:
                    self.cur_anim = self.purple_falling_left_frames
                else:
                    self.cur_anim = self.purple_falling_right_frames
            if initial_anim == self.purple_falling_left_frames or initial_anim == self.purple_falling_right_frames:
                if self.anim_index >= 1:
                    self.anim_index = 1
        elif not self.is_falling and (initial_anim == self.purple_falling_left_frames or initial_anim == self.purple_falling_right_frames):
            if initial_anim == self.purple_falling_left_frames or initial_anim == self.purple_falling_right_frames:
                if self.anim_index < 4:
                    if self.facing_left:
                        self.cur_anim = self.purple_falling_left_frames
                    else:
                        self.cur_anim = self.purple_falling_right_frames
            else:
                self.is_idle = True
                if self.facing_left:
                    self.cur_anim = self.purple_idle_left_frames
                else:
                    self.cur_anim = self.purple_idle_right_frames

    # player movement left and right and the player's jump
    # makes sure that the player can only jump when on land or less than 6 frames after
    def movement(self):
        self.player_movement = [0, 0]
        if self.moving_right:
            self.player_movement[0] += 2
        if self.moving_left:
            self.player_movement[0] += -2
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.4
        if self.player_y_momentum > 5:
            self.player_y_momentum = 5
        if not self.is_jumping and self.player_y_momentum < 0:
            self.player_y_momentum = 0

    def becomes_colourful(self):
        self.is_colourful = True
        self.colour_index = 0
        self.player_colours['blue'] = True

    # changes the colour of the sprite when the player holds down left shift
    # should also highlight the colour wheel on the top left but i havent done that yet
    '''
    def change_colour(self):
        if self.colour_index == 0:
            self.player_colours['blue'], self.player_colours['green'], self.player_colours['purple'] = True, False, False
            if self.is_idle:
                if self.facing_right:
                    self.cur_anim = self.blue_idle_right_frames
                elif self.facing_left:
                    self.cur_anim = self.blue_idle_left_frames
        elif self.colour_index == 1:
            self.player_colours['green'], self.player_colours['purple'], self.player_colours['blue'] = True, False, False
            if self.is_idle:
                if self.facing_right:
                    self.cur_anim = self.green_idle_right_frames
                elif self.facing_left:
                    self.cur_anim = self.green_idle_left_frames
        elif self.colour_index == 2:
            self.player_colours['purple'], self.player_colours['green'], self.player_colours['blue'] = True, False, False
            if self.is_idle:
                if self.facing_right:
                    self.cur_anim = self.purple_idle_right_frames
                elif self.facing_left:
                    self.cur_anim = self.purple_idle_left_frames
    '''
    # def get_player_colour(self):
    def change_colour(self):
        if self.colour_index == 0:
            self.player_colours['blue'], self.player_colours['green'], self.player_colours['purple'] = True, False, False
            self.blue_anim()
        elif self.colour_index == 1:
            self.player_colours['green'], self.player_colours['purple'], self.player_colours['blue'] = True, False, False
            self.green_anim()
        elif self.colour_index == 2:
            self.player_colours['purple'], self.player_colours['green'], self.player_colours['blue'] = True, False, False
            self.purple_anim()

    def change_frame(self, anim_count, idle_count):
        initial_anim = self.cur_anim
        if anim_count >= 5:
            if self.is_jumping:
                self.anim_index += 1
                if self.anim_index >= 2:
                    self.anim_index = 2
                    return
            elif self.is_falling:
                if self.anim_index >= 4:
                    self.anim_index = 4
            elif self.anim_index >= len(self.cur_anim) - 1:
                self.anim_index = 0
            else:
                self.anim_index += 1
        if idle_count < 240 and (self.cur_anim == self.default_idle_left_frames or self.cur_anim == self.default_idle_right_frames
                                 or self.cur_anim == self.blue_idle_left_frames or self.cur_anim == self.blue_idle_right_frames
                                 or self.cur_anim == self.green_idle_left_frames or self.cur_anim == self.green_idle_right_frames
                                 or self.cur_anim == self.purple_idle_left_frames or self.cur_anim == self.purple_idle_right_frames):
            self.anim_index = 0

    # detracts health from player after calculating the damage
    def take_damage(self, rect):
        self.health -= self.calc_damage(self, rect)
        if self.health <= 0:
            self.respawn(self.player_movement)

    # def deal_damage(self, rect):

    # returns amount of damage from collision based on the colour system
    def calc_damage(self, rect):
        if self.player_colours['blue']:
            if rect.colour == 'red' or rect.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.player_colours['green']:
            if rect.colour == 'orange' or rect.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.player_colours['purple']:
            if rect.colour == 'red' or rect.colour == 'orange':
                self.damage = 1
            else:
                self.damage = 2
        else:
            self.damage = 1

    # refills player's health and returns them back to their last save point
    def respawn(self, respawn_point):
        self.health = 10

    def update(self, anim_count, idle_count):
        self.movement()
        self.change_frame(anim_count, idle_count)
        self.animations()
