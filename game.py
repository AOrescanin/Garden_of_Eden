import pygame

import snake
import fruit
import wall
import screen

# Animate the fruit, add a better score board, display the score at the end, ask user if they want to play again or go
# to main menu, make sure walls dont spawn too near the snake, fix the animation of the snake in the no
# walls game mode, fix adjacent wall spawn visual bug(similar to original golden fruit bug), fix sound effects canceling
# each other out, add comments and clean up code, add wall placement sound effect, add snake hits itself sound effect,
# fix mushroom controls updating a couple frames late

# **********************************************************************************************************************

class Game:

    def __init__(self):
        pygame.init()

        self.SCREEN_UPDATE = pygame.USEREVENT
        self.no_walls_game_mode = False
        self.adjacent_wall = False
        self.INITIAL_BODY_LENGTH = 3
        self.score = 0
        self.score_tracker = 3
        self.game_font = pygame.font.Font(None, 24)
        self.is_high = False
        self.temp_body_len = 0

        self.screen = screen.Screen()
        self.snake = snake.Snake()
        self.fruit = fruit.Fruit()
        self.wall = wall.Wall()

# **********************************************************************************************************************

    def update(self):
        self.check_collision()
        self.snake.move_snake()
        self.check_fail()

# **********************************************************************************************************************

    def set_response_time(self, response_time):
        pygame.time.set_timer(self.SCREEN_UPDATE, response_time)

# **********************************************************************************************************************

    def draw_elements(self):
        self.draw_grass()

        if int(len(self.snake.body) - self.INITIAL_BODY_LENGTH) % 15 == 14:
            self.fruit.draw_mushroom()

        elif (int(len(self.snake.body)) > 10) and \
                    ((int(len(self.snake.body) - self.INITIAL_BODY_LENGTH)) % 11 == 0):
            self.fruit.draw_x2_fruit()

        else:
            self.fruit.draw_fruit()

        self.snake.draw_snake()
        self.draw_score()

        if self.wall.game_mode_selected == True:
            for block in self.wall.wall_list[1:]:  # This seems to work for stopping adjacent blocks from spawning but I think it makes more sense in check collision and there is a visual bug where the adjacent wall is shown for a millisecond before respawning
                if (self.wall.wall_list[0].x == block.x and self.wall.wall_list[0].y == block.y) \
                    or (self.wall.wall_list[0].x + 1 == block.x and self.wall.wall_list[0].y == block.y) \
                    or (self.wall.wall_list[0].x - 1 == block.x and self.wall.wall_list[0].y == block.y) \
                    or (self.wall.wall_list[0].y + 1 == block.y and self.wall.wall_list[0].x == block.x) \
                    or (self.wall.wall_list[0].y - 1 == block.y and self.wall.wall_list[0].x == block.x) \
                    or (self.wall.wall_list[0].x + 1 == block.x and self.wall.wall_list[0].y + 1 == block.y) \
                    or (self.wall.wall_list[0].x + 1 == block.x and self.wall.wall_list[0].y - 1 == block.y) \
                    or (self.wall.wall_list[0].x - 1 == block.x and self.wall.wall_list[0].y + 1 == block.y) \
                    or (self.wall.wall_list[0].x - 1 == block.x and self.wall.wall_list[0].y - 1 == block.y):
                    self.wall.wall_list.pop(0)
                    self.wall.randomize()
                    self.wall.add_block()

            self.wall.draw_wall()

# **********************************************************************************************************************

    def draw_grass(self):
        grass_color1 = (171, 216, 72)
        grass_color2 = (162, 206, 63)

        self.screen.display.fill(grass_color1)

        for row in range(self.screen.CELL_NUMBER):
            if (row % 2) == 0:
                for col in range(self.screen.CELL_NUMBER):
                    if (col % 2) == 0:
                        grass_rect = pygame.Rect((col * self.screen.CELL_SIZE), (row * self.screen.CELL_SIZE),
                                                 self.screen.CELL_SIZE, self.screen.CELL_SIZE)
                        pygame.draw.rect(self.screen.display, grass_color2, grass_rect)

            else:
                for col in range(self.screen.CELL_NUMBER):
                    if (col % 2) == 1:
                        grass_rect = pygame.Rect((col * self.screen.CELL_SIZE), (row * self.screen.CELL_SIZE),
                                                 self.screen.CELL_SIZE, self.screen.CELL_SIZE)
                        pygame.draw.rect(self.screen.display, grass_color2, grass_rect)

# **********************************************************************************************************************

    def draw_score(self):
        self.score = str(len(self.snake.body) - self.score_tracker)
        font_color = (33, 33, 33)
        score_surface = self.game_font.render(self.score, True, font_color)
        score_x = int(self.screen.CELL_SIZE - 33)
        score_y = int(self.screen.CELL_SIZE - 27)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        self.screen.display.blit(score_surface, score_rect)

# **********************************************************************************************************************

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            if int(len(self.snake.body) > self.temp_body_len):
                self.is_high = False

            if (int(len(self.snake.body)) > self.INITIAL_BODY_LENGTH) and \
                    ((int((len(self.snake.body) - self.INITIAL_BODY_LENGTH)) % 15) == 14):
                self.score_tracker -= 3
                self.is_high = True
                self.temp_body_len = int(len(self.snake.body))
                self.snake.play_mushroom_sound()

            if (int(len(self.snake.body)) > 10) and \
                    (((int(len(self.snake.body) - self.INITIAL_BODY_LENGTH)) % 11) == 0):
                self.score_tracker -= 1
                self.snake.play_level_up_sound()
                self.response_time -= 10

            if self.wall.game_mode_selected == True:
                if (int(len(self.snake.body)) % 2) == 0:
                    self.wall.randomize()
                    self.wall.add_block()

            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_eat_sound()

        for block in self.snake.body[1:]:  # make sure a fruit does not spawn on top of the snake
            if block == self.fruit.position:
                self.fruit.randomize()

        if self.wall.game_mode_selected == True:
            for block in self.wall.wall_list[:]:  # make sure a fruit does not spawn on top of a wall
                if block == self.fruit.position:
                    self.fruit.randomize()

            for block in self.snake.body[:]:  # make sure wall does not spawn in the body of the snake
                if block == self.wall.position:
                    self.wall.randomize()

# **********************************************************************************************************************

    def check_fail(self):
        if self.no_walls_game_mode == False:
            if not 0 <= self.snake.body[0].x < self.screen.CELL_NUMBER \
                    or not 0 <= self.snake.body[0].y < self.screen.CELL_NUMBER:  # if the snake goes out of bounds
                self.wall.play_wall_collision_sound()
                self.game_over()

        else:
            if self.snake.body[0].x == self.screen.CELL_NUMBER:
                self.snake.body[0].x = 0
            if self.snake.body[0].x < 0:
                self.snake.body[0].x = self.screen.CELL_NUMBER
            if self.snake.body[0].y == self.screen.CELL_NUMBER:
                self.snake.body[0].y = 0
            if self.snake.body[0].y < 0:
                self.snake.body[0].y = self.screen.CELL_NUMBER

        for block in self.snake.body[1:]:  # if the snake hits itself
            if block == self.snake.body[0]:
                self.game_over()

        if self.wall.game_mode_selected == True:
            for block in self.wall.wall_list:  # if the snake hits the wall
                if block == self.snake.body[0]:
                    self.wall.play_wall_collision_sound()
                    self.game_over()

# **********************************************************************************************************************

    def game_over(self):
        self.score_tracker = self.INITIAL_BODY_LENGTH
        self.response_time = 150
        self.snake.reset_game()
        self.wall.reset_game()
        self.is_high = False
