import pygame
import main
from sys import exit
pygame.init()
newScreen = main.screen


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pBlue = pygame.draw.rect(newScreen, 'Blue', (200,200))
        pGreen = pygame.draw.rect(newScreen, 'Green', (200,200))
        pPurple = pygame.draw.rect(newScreen, 'Purple', (200,200))
        self.playerColours = [pBlue, pGreen, pPurple]

    def playerInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.changeColour()
                if event.key == pygame.K_RIGHT:


    def changeColour(self):




