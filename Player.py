import pygame

RED = (255, 0, 0)


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.color = RED
        self.x = 70
        self.y = 40
        self.width = 20
        self.height = 20

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.width, self.height])

    def update(self):
        pass