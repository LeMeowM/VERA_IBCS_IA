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

        # colour state
        self.is_changing_colour: bool = False
        default_state: pygame.image = pygame.image.load('../player_default.png').convert_alpha()
        self.player_colours: dict = {'blue': True, 'green': False, 'purple': False}
        self.colour_index: int = 3
        self.damage: int = 0
        self.idle_count: int = 0

        self.default_anim_frames: list = []
        self.default_idle_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_idle_left/', 'player_default_idle_left',
                            self.default_idle_left_frames)
        self.default_idle_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_idle_right/', 'player_default_idle_right',
                            self.default_idle_right_frames)
        self.default_moving_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_moving_right/',
                            'player_default_moving_right',
                            self.default_moving_right_frames)
        self.default_moving_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_moving_left/', 'player_default_moving_left',
                            self.default_moving_left_frames)
        self.default_jumping_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_jumping_left/',
                            'player_default_jumping_left',
                            self.default_jumping_left_frames)
        self.default_falling_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_falling_left/',
                            'player_default_falling_left',
                            self.default_falling_left_frames)
        self.default_jumping_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_jumping_right/',
                            'player_default_jumping_right',
                            self.default_jumping_right_frames)
        self.default_falling_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_default_anim/player_default_falling_right/',
                            'player_default_falling_right', self.default_falling_right_frames)
        self.default_attack_left_frames: list = []
        # load_image_from_gif('player_anim/player_default_anim/player_default_attack_vfx/', 'attack_vfx_anim', self.default_attack_left_frames)
        self.default_damaged_frames: list = []

        self.blue_anim_frames: list = []
        self.blue_idle_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_idle_left/', 'player_blue_idle_left',
                            self.blue_idle_left_frames)
        self.blue_idle_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_idle_right/', 'player_blue_idle_right',
                            self.blue_idle_right_frames)
        self.blue_moving_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_moving_right/', 'player_blue_moving_right',
                            self.blue_moving_right_frames)
        self.blue_moving_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_moving_left/', 'player_blue_moving_left',
                            self.blue_moving_left_frames)
        self.blue_jumping_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_jumping_left/', 'player_blue_jumping_left',
                            self.blue_jumping_left_frames)
        self.blue_falling_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_falling_left/',
                            'player_blue_falling_left', self.blue_falling_left_frames)
        self.blue_jumping_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_jumping_right/', 'player_blue_jumping_right',
                            self.blue_jumping_right_frames)
        self.blue_falling_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_blue_anim/player_blue_falling_right/',
                            'player_blue_falling_right', self.blue_falling_right_frames)
        self.blue_attacking_frames: list = []
        self.blue_damaged_frames: list = []

        self.green_anim_frames: list = []
        self.green_idle_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_idle_left/', 'player_green_idle_left',
                            self.green_idle_left_frames)
        self.green_idle_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_idle_right/', 'player_green_idle_right',
                            self.green_idle_right_frames)
        self.green_moving_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_moving_right/', 'player_green_moving_right',
                            self.green_moving_right_frames)
        self.green_moving_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_moving_left/', 'player_green_moving_left',
                            self.green_moving_left_frames)
        self.green_jumping_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_jumping_left/', 'player_green_jumping_left',
                            self.green_jumping_left_frames)
        self.green_falling_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_falling_left/',
                            'player_green_falling_left', self.green_falling_left_frames)
        self.green_jumping_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_jumping_right/', 'player_green_jumping_right',
                            self.green_jumping_right_frames)
        self.green_falling_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_green_anim/player_green_falling_right/',
                            'player_green_falling_right', self.green_falling_right_frames)
        self.green_attacking_frames: list = []
        self.green_damaged_frames: list = []

        self.purple_anim_frames: list = []
        self.purple_idle_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_idle_left/', 'player_purple_idle_left',
                            self.purple_idle_left_frames)
        self.purple_idle_right_frames = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_idle_right/', 'player_purple_idle_right',
                            self.purple_idle_right_frames)
        self.purple_moving_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_moving_right/', 'player_purple_moving_right',
                            self.purple_moving_right_frames)
        self.purple_moving_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_moving_left/', 'player_purple_moving_left',
                            self.purple_moving_left_frames)
        self.purple_jumping_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_jumping_left/', 'player_purple_jumping_left',
                            self.purple_jumping_left_frames)
        self.purple_falling_left_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_falling_left/',
                            'player_purple_falling_left', self.purple_falling_left_frames)
        self.purple_jumping_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_jumping_right/',
                            'player_purple_jumping_right',
                            self.purple_jumping_right_frames)
        self.purple_falling_right_frames: list = []
        load_image_from_gif('../resources/textures/player_anim/player_purple_anim/player_purple_falling_right/',
                            'player_purple_falling_right', self.purple_falling_right_frames)
        self.purple_attacking_frames: list = []
        self.purple_damaged_frames: list = []

        self.cur_anim: list = self.default_idle_left_frames
        self.anim_index: int = 0
        self.image: pygame.image = self.cur_anim[self.anim_index]

        # player location and movement variables
        self.facing_left: bool = False
        self.facing_right: bool = False
        self.is_idle: bool = False
        self.moving_right: bool = False
        self.moving_left: bool = False
        self.is_jumping: bool = False
        self.is_falling: bool = False
        self.is_attack: bool = False
        self.is_hit: bool = False
        self.init_move: bool = self.moving_left
        self.player_y_momentum: int = 0
        self.player_x_momentum: int = 0
        self.player_movement: list = [0, 0]
        self.health: int = 6
        self.air_timer: int = 0

        self.rect: pygame.Rect = pygame.Rect(50, 0, default_state.get_width() - 6, default_state.get_height())
        self.damage_cooldown: int = 120
        self.attack_cooldown: int = 30

        self.attack_vfx_full = pygame.image.load(
            '../resources/textures/player_anim/player_default_anim/player_default_attack_vfx/attack_vfx_anim_left/attack_vfx_left_anim_1.png').convert_alpha()
        self.attack_left: list = []
        load_image_from_gif(
            '../resources/textures/player_anim/player_default_anim/player_default_attack_vfx/attack_vfx_anim_left/',
                            'attack_vfx_left_anim', self.attack_left)
        self.attack_right: list = []
        load_image_from_gif(
            '../resources/textures/player_anim/player_default_anim/player_default_attack_vfx/attack_vfx_anim_right/',
                            'attack_vfx_right_anim', self.attack_right)
        self.attack_index: int = 2

        self.cur_attack_anim: list = self.attack_left
        self.attack_image: pygame.image = self.cur_attack_anim[self.attack_index]
        self.attack_rect: pygame.Rect = pygame.Rect(50, 0, self.attack_vfx_full.get_width(), self.attack_vfx_full.get_height())
        self.attack_hit: bool = False
        self.attack_hit_left_frames: list = []
        load_image_from_gif(
            '../resources/textures/player_anim/player_default_anim/player_default_attack_vfx/attack_hit_anim_left/',
                            'attack_hit_left_anim', self.attack_hit_left_frames)
        self.attack_hit_right_frames: list = []
        load_image_from_gif(
            '../resources/textures/player_anim/player_default_anim/player_default_attack_vfx/attack_hit_anim_right/',
                            'attack_hit_right_anim', self.attack_hit_right_frames)
        self.attack_hit_index: int = 0
        self.cur_attack_hit_anim: list = self.attack_hit_right_frames
        self.attack_hit_image: pygame.image = self.cur_attack_hit_anim[self.attack_hit_index]


    def draw(self, display, scroll):
        self.image = self.cur_anim[self.anim_index]
        self.attack_image = self.cur_attack_anim[self.attack_index]
        display.blit(self.image, (self.rect.x - 3 - scroll[0], self.rect.y - scroll[1]))
        display.blit(self.attack_image, (self.attack_rect.x - scroll[0], self.attack_rect.y - scroll[1]))
        self.attack_hit_image = self.cur_attack_hit_anim[self.attack_hit_index]
        display.blit(self.attack_hit_image, (self.attack_rect.x - scroll[0], self.attack_rect.y - scroll[1]))


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

    def animations(self) -> None:
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
        if self.attack_hit:
            if self.facing_left:
                self.cur_attack_hit_anim = self.attack_hit_left_frames
            else:
                self.cur_attack_hit_anim = self.attack_hit_right_frames
            if self.attack_cooldown >= 5:
                self.attack_hit = False


    def default_anim(self) -> None:
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
        elif not self.is_falling and (
                initial_anim == self.default_falling_left_frames or initial_anim == self.default_falling_right_frames):
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

    def blue_anim(self) -> None:
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
        elif not self.is_falling and (
                initial_anim == self.blue_falling_left_frames or initial_anim == self.blue_falling_right_frames):
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

    def green_anim(self) -> None:
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
        elif not self.is_falling and (
                initial_anim == self.green_falling_left_frames or initial_anim == self.green_falling_right_frames):
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

    def purple_anim(self) -> None:
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
        elif not self.is_falling and (
                initial_anim == self.purple_falling_left_frames or initial_anim == self.purple_falling_right_frames):
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
    def movement(self) -> None:
        self.player_movement = [0, 0]
        if self.moving_right:
            if self.init_move == self.moving_left:
                self.player_x_momentum = 0
            self.player_movement[0] += self.player_x_momentum
            self.player_x_momentum += 0.4
            if self.player_x_momentum > 2:
                self.player_x_momentum = 2
        if self.moving_left:
            if self.init_move == self.moving_right:
                self.player_x_momentum = 0
            self.player_movement[0] += self.player_x_momentum
            self.player_x_momentum += -0.4
            if self.player_x_momentum < -2:
                self.player_x_momentum = -2
        if not self.moving_right and not self.moving_left:
            self.player_x_momentum = 0
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.4
        if self.player_y_momentum > 5:
            self.player_y_momentum = 5
        if not self.is_jumping and self.player_y_momentum < 0:
            self.player_y_momentum = 0.5

    def becomes_colourful(self) -> None:
        self.is_colourful = True
        self.colour_index = 0
        self.player_colours['blue'] = True

    # changes the colour of the sprite when the player holds down left shift
    # def get_player_colour(self):
    def change_colour(self) -> None:
        if self.colour_index == 0:
            self.player_colours['blue'], self.player_colours['green'], self.player_colours[
                'purple'] = True, False, False
            self.blue_anim()
        elif self.colour_index == 1:
            self.player_colours['green'], self.player_colours['purple'], self.player_colours[
                'blue'] = True, False, False
            self.green_anim()
        elif self.colour_index == 2:
            self.player_colours['purple'], self.player_colours['green'], self.player_colours[
                'blue'] = True, False, False
            self.purple_anim()

    def change_frame(self, anim_count: int, idle_count: int) -> None:
        if anim_count >= 5:
            if self.attack_index < 4:
                self.attack_index += 1
            if self.attack_hit_index < 3 and self.attack_hit:
                self.attack_hit_index += 1
            else:
                self.attack_hit_index = 0
                self.attack_hit = False
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
        if idle_count < 240 and (self.cur_anim == self.default_idle_left_frames
                                 or self.cur_anim == self.default_idle_right_frames
                                 or self.cur_anim == self.blue_idle_left_frames
                                 or self.cur_anim == self.blue_idle_right_frames
                                 or self.cur_anim == self.green_idle_left_frames
                                 or self.cur_anim == self.green_idle_right_frames
                                 or self.cur_anim == self.purple_idle_left_frames
                                 or self.cur_anim == self.purple_idle_right_frames):
            self.anim_index = 0

    # detracts health from player after calculating the damage
    def take_damage(self, room_enemies: list) -> None:
        for enemy in room_enemies:
            if pygame.Rect.colliderect(self.rect, enemy.rect) and not room_enemies[enemy]:
                if self.damage_cooldown >= 120:
                    self.calc_damage(enemy)
                    self.health -= self.damage
                    self.damage_cooldown = 0
        if self.health < 0:
            self.health = 6
        self.damage_cooldown += 1

    def attack(self, room_enemies: list) -> None:
        if self.is_attack and self.attack_cooldown >= 30:
            self.attack_index = 0
            self.attack_cooldown = 0
            if self.facing_left:
                self.cur_attack_anim = self.attack_left
            else:
                self.cur_attack_anim = self.attack_right
            self.deal_damage(room_enemies)
        else:
            self.attack_index = 4
            self.attack_cooldown += 1
        if self.facing_left:
            self.attack_rect.x = self.rect.x - 25
            self.attack_rect.y = self.rect.y
        else:
            self.attack_rect.x = self.rect.x + 10
            self.attack_rect.y = self.rect.y

    def deal_damage(self, room_enemies: list) -> None:
        for enemy in room_enemies:
            if pygame.Rect.colliderect(self.attack_rect, enemy.rect) and not enemy.is_dead:
                self.calc_damage(enemy)
                enemy.health -= self.damage
                enemy.x_momentum = 5
                enemy.y_momentum = 5
                if not enemy.is_dead:
                    if self.facing_left:
                        self.player_x_momentum += 5
                    else:
                        self.player_x_momentum -= 5
                self.attack_hit = True


    # returns amount of damage from collision based on the colour system

    def calc_damage(self, enemy: pygame.sprite) -> None:
        if self.player_colours['blue']:
            if enemy.colour == 'red' or enemy.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.player_colours['green']:
            if enemy.colour == 'orange' or enemy.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.player_colours['purple']:
            if enemy.colour == 'red' or enemy.colour == 'orange':
                self.damage = 1
            else:
                self.damage = 2
        else:
            self.damage = 1

    # refills player's health and returns them back to their last save point
    def respawn(self):
        self.health = 6

    def update(self, anim_count: int, idle_count: int, enemies: list):
        self.movement()
        self.change_frame(anim_count, idle_count)
        self.animations()
        self.attack(enemies)
        self.take_damage(enemies)
