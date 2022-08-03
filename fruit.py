import random
import pygame
from pygame.math import Vector2

import screen

# **********************************************************************************************************************

class Fruit:
    pygame.init()

    def __init__(self):
        self.screen = screen.Screen()
        self.x = 0
        self.y = 0
        self.position = Vector2(self.x, self.y)

        self.apple = pygame.image.load('assets/apple.png').convert_alpha()
        self.golden_apple = pygame.image.load('assets/golden_apple.png').convert_alpha()
        self.mushroom = pygame.image.load('assets/mushroom.png').convert_alpha()

        self.randomize()

# **********************************************************************************************************************

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * self.screen.CELL_SIZE),
                                 int(self.position.y * self.screen.CELL_SIZE),
                                 self.screen.CELL_SIZE, self.screen.CELL_SIZE)

        self.screen.display.blit(self.apple, fruit_rect)

# **********************************************************************************************************************

    def draw_x2_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * self.screen.CELL_SIZE),
                                 int(self.position.y * self.screen.CELL_SIZE),
                                 self.screen.CELL_SIZE, self.screen.CELL_SIZE)

        self.screen.display.blit(self.golden_apple, fruit_rect)

# **********************************************************************************************************************

    def draw_mushroom(self):
        mushroom_rect = pygame.Rect(int(self.position.x * self.screen.CELL_SIZE),
                                 int(self.position.y * self.screen.CELL_SIZE),
                                 self.screen.CELL_SIZE, self.screen.CELL_SIZE)

        self.screen.display.blit(self.mushroom, mushroom_rect)

# **********************************************************************************************************************

    def randomize(self):
        self.x = random.randint(0, (self.screen.CELL_NUMBER - 1))
        self.y = random.randint(0, (self.screen.CELL_NUMBER - 1))
        self.position = Vector2(self.x, self.y)
