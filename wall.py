import random
import pygame
from pygame.math import Vector2

import screen

# **********************************************************************************************************************

class Wall:
    pygame.init()

    def __init__(self):
        self.screen = screen.Screen()
        self.game_mode_selected = False
        self.new_block = False
        self.x = -1
        self.y = -1
        self.position = Vector2(self.x, self.y)
        self.wall_list = [self.position]
        self.wall_num = -1

        self.wall = pygame.image.load('assets/wall.png').convert_alpha()
        self.wall_collision_sound = pygame.mixer.Sound('assets/collision.wav')

# **********************************************************************************************************************

    def set_game_mode_on(self):
        self.game_mode_selected = True

    def draw_wall(self):
        if self.new_block == True:
            self.wall_list.insert(0, self.position)
            self.wall_num += 1
            self.new_block = False

        for index, block in enumerate(self.wall_list):  # continue to spawn all the walls up to this point
            if index >= 0:
                x_position = int(block.x * self.screen.CELL_SIZE)
                y_position = int(block.y * self.screen.CELL_SIZE)
                wall_rect = pygame.Rect(x_position, y_position, self.screen.CELL_SIZE, self.screen.CELL_SIZE)

                self.screen.display.blit(self.wall, wall_rect)

# **********************************************************************************************************************

    def add_block(self):
        self.new_block = True

# **********************************************************************************************************************

    def play_wall_collision_sound(self):
        self.wall_collision_sound.play()

# **********************************************************************************************************************

    def randomize(self):
        self.x = random.randint(0, (self.screen.CELL_NUMBER - 1))
        self.y = random.randint(0, (self.screen.CELL_NUMBER - 1))
        self.position = Vector2(self.x, self.y)

# **********************************************************************************************************************

    def reset_game(self):
        self.new_block = False
        self.wall_list = []
