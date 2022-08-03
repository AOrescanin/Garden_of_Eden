import pygame

# **********************************************************************************************************************

class Screen:
    def __init__(self):
        pygame.init()

        self.CELL_SIZE = 40
        self.CELL_NUMBER = 16
        self.display = pygame.display.set_mode(((self.CELL_NUMBER * self.CELL_SIZE),
                                                (self.CELL_NUMBER * self.CELL_SIZE)))
