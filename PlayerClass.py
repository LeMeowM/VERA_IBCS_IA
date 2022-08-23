import pygame
from sys import exit

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # colour states
        self.isBlue = False
        self.isGreen = False
        self.isPurple = False
        self.is_colourful = False
        self.is_changing_colour = False
        default_state = pygame.image.load('player_default.png').convert_alpha()
        blue_state = pygame.image.load('player_blue.png').convert_alpha()
        green_state = pygame.image.load('player_green.png').convert_alpha()
        purple_state = pygame.image.load('player_purple.png').convert_alpha()
        self.player_colours = [blue_state, green_state, purple_state]
        self.colour_index = 0
        self.image = default_state
        self.damage = 0

        # player location and movement variables
        self.moving_right = False
        self.moving_left = False
        self.player_y_momentum = 0
        self.player_x_momentum = 0
        self.player_movement = [0, 0]
        self.health = 10
        self.air_timer = 0
        self.is_jumping = False
        self.rect = pygame.Rect(50, 0, default_state.get_width(), default_state.get_height())

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

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
                    self.player_y_momentum = -5
                    self.is_jumping = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                if event.key == pygame.K_UP:
                    self.is_jumping = False

    # player movement left and right and the player's jump
    # makes sure that the player can only jump when on land or less than 6 frames after
    def movement(self):
        if self.moving_right:
            self.player_movement[0] += 2
        if self.moving_left:
            self.player_movement[0] += -2
        self.player_movement[1] += self.player_y_momentum
        self.player_y_momentum += 0.4
        if self.player_y_momentum > 5:
            self.player_y_momentum = 5
        if not self.is_jumping and self.player_y_momentum < 0:
            self.player_y_momentum = 1

    def becomes_colourful(self):
        self.is_colourful = True
        self.image = self.player_colours[self.colour_index]

    # changes the colour of the sprite when the player holds down left shift
    # should also highlight the colour wheel on the top left but i havent done that yet
    def change_colour(self):
        self.image = self.player_colours[self.colour_index]

    # detracts health from player after calculating the damage
    def take_damage(self, rect):
        self.health -= self.calc_damage(self, rect)
        if self.health <= 0:
            self.respawn(self.player_movement)

    # def deal_damage(self, rect):

    # returns amount of damage from collision based on the colour system
    def calc_damage(self, rect):
        if self.isBlue:
            if rect.colour == 'red' or rect.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.isGreen:
            if rect.colour == 'orange' or rect.colour == 'yellow':
                self.damage = 1
            else:
                self.damage = 2
        elif self.isPurple:
            if rect.colour == 'red' or rect.colour == 'orange':
                self.damage = 1
            else:
                self.damage = 2
        else:
            self.damage = 1

    # refills player's health and returns them back to their last save point
    def respawn(self, respawn_point):
        self.health = 10

    def update(self):
        self.movement()
        self.change_colour()
