import pygame
pygame.display.set_mode()


class GameUI:
    def __init__(self):
        self.changing_blue = pygame.image.load(
            '../../resources/textures/ui/changing_colour_ui/changing_blue_ui.png').convert_alpha()
        self.changing_green = pygame.image.load(
            '../../resources/textures/ui/changing_colour_ui/changing_green_ui.png').convert_alpha()
        self.changing_purple = pygame.image.load(
            '../../resources/textures/ui/changing_colour_ui/changing_purple_ui.png').convert_alpha()
        self.changing_colour_ui = [self.changing_blue, self.changing_green, self.changing_purple]

        self.colours = pygame.image.load('../../resources/textures/ui/colour_ui.png').convert_alpha()
        self.colour_line = pygame.image.load('../../resources/textures/ui/colour_line_ui.png').convert_alpha()
        self.cur_colour_line = self.colour_line
        self.colour_index = 0

        self.default_health_full = pygame.image.load(
            '../../resources/textures/ui/default_health/default_full_health_ui.png').convert_alpha()
        self.default_health_5 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_5_health_ui.png').convert_alpha()
        self.default_health_4 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_4_health_ui.png').convert_alpha()
        self.default_health_3 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_3_health_ui.png').convert_alpha()
        self.default_health_2 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_2_health_ui.png').convert_alpha()
        self.default_health_1 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_1_health_ui.png').convert_alpha()
        self.default_health_0 = pygame.image.load(
            '../../resources/textures/ui/default_health/default_0_health_ui.png').convert_alpha()
        self.default_health_ui = [self.default_health_0, self.default_health_1, self.default_health_2, self.default_health_3, self.default_health_4, self.default_health_5,
                          self.default_health_full]
        self.default_ui = pygame.image.load('../../resources/textures/ui/default_state_ui.png').convert_alpha()

        self.health_full = pygame.image.load('../../resources/textures/ui/health_ui/full_health_ui.png').convert_alpha()
        self.health_5 = pygame.image.load('../../resources/textures/ui/health_ui/5_health_ui.png').convert_alpha()
        self.health_4 = pygame.image.load('../../resources/textures/ui/health_ui/4_health_ui.png').convert_alpha()
        self.health_3 = pygame.image.load('../../resources/textures/ui/health_ui/3_health_ui.png').convert_alpha()
        self.health_2 = pygame.image.load('../../resources/textures/ui/health_ui/2_health_ui.png').convert_alpha()
        self.health_1 = pygame.image.load('../../resources/textures/ui/health_ui/1_health_ui.png').convert_alpha()
        self.health_0 = pygame.image.load('../../resources/textures/ui/health_ui/0_health_ui.png').convert_alpha()
        self.health_ui = [self.health_0, self.health_1, self.health_2, self.health_3, self.health_4, self.health_5, self.health_full]
        self.health = 6
        self.cur_health = self.health_ui[self.health]
        self.power_line= pygame.image.load('../../resources/textures/ui/power_line_ui.png').convert_alpha()
        self.loc = [8, 0]

    def draw(self, display, player):
        self.change_health(player)
        if player.is_colourful:
            display.blit(self.colours, self.loc)
            display.blit(self.cur_health, self.loc)
            display.blit(self.cur_colour_line, self.loc)
            display.blit(self.power_line, self.loc)
        else:
            display.blit(self.cur_health, self.loc)
            display.blit(self.default_ui, self.loc)

    def change_colour(self, player, colour_index):
        if not player.is_changing_colour:
            self.cur_colour_line = self.colour_line
        else:
            self.colour_index = colour_index

    def change_health(self, player):
        self.health = player.health
        if player.is_colourful:
            self.cur_health = self.health_ui[self.health]
        else:
            self.cur_health = self.default_health_ui[self.health]






