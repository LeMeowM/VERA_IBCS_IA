import pygame
pygame.display.set_mode()


class GameUI:
    def __init__(self):
        self.changing_blue = pygame.image.load('ui/changing_colour_ui/changing_blue_ui.png').convert_alpha()
        self.changing_green = pygame.image.load('ui/changing_colour_ui/changing_green_ui.png').convert_alpha()
        self.changing_purple = pygame.image.load('ui/changing_colour_ui/changing_purple_ui.png').convert_alpha()
        self.changing_colour_ui = [self.changing_blue, self.changing_green, self.changing_purple]

        self.colours = pygame.image.load('ui/colour_ui.png').convert_alpha()
        self.colour_line = pygame.image.load('ui/colour_line_ui.png').convert_alpha()
        self.cur_colour_line = self.colour_line
        self.colour_index = 0

        self.health_full = pygame.image.load('ui/health_ui/full_health_ui.png').convert_alpha()
        self.health_5 = pygame.image.load('ui/health_ui/5_health_ui.png').convert_alpha()
        self.health_4 = pygame.image.load('ui/health_ui/4_health_ui.png').convert_alpha()
        self.health_3 = pygame.image.load('ui/health_ui/3_health_ui.png').convert_alpha()
        self.health_2 = pygame.image.load('ui/health_ui/2_health_ui.png').convert_alpha()
        self.health_1 = pygame.image.load('ui/health_ui/1_health_ui.png').convert_alpha()
        self.health_0 = pygame.image.load('ui/health_ui/0_health_ui.png').convert_alpha()
        self.health_ui = [self.health_0, self.health_1, self.health_2, self.health_3, self.health_4, self.health_5, self.health_full]
        self.health = 6
        self.cur_health = self.health_ui[self.health]
        self.power_line= pygame.image.load('ui/power_line_ui.png').convert_alpha()

    def draw(self, display):
        display.blit(self.colours, [0, 0])
        display.blit(self.cur_health, [0, 0])
        display.blit(self.cur_colour_line, [0, 0])
        display.blit(self.power_line, [0, 0])

    def change_colour(self, player, colour_index):
        if not player.is_changing_colour:
            self.cur_colour_line = self.colour_line
        else:
            self.colour_index = colour_index






