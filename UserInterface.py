import pygame, sys

class UserInterface:
    def __init__(self):

    def main_menu(self, display):
        while True:
            display.fill('black')
            play_button = pygame.Rect(60, 60, 200, 50)
            quit_button = pygame.Rect(60, 120, 200, 50)
            m_x, m_y = pygame.mouse.get_pos()

            pygame.draw.rect(display, 'blue', play_button)
            pygame.draw.rect(display, 'blue', quit_button)

            if play_button.collidepoint(m_x, m_y):

class Button(pygame.sprite.Sprite):
    def __init__(self, image, text, location):
        super().__init__()
        self.is_mouse_hover = False
        self.image = image
        self.text = text
        self.rect = pygame.Rect(location[0], location[1], image.get_width(), image.get_height())
        self.rect_scaled

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        display.blit(self.text, self.text.get_rect())
