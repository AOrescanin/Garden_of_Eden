import sys
import pygame
from pygame.math import Vector2

import screen
import button
import game

# **********************************************************************************************************************

class Menu:
    def __init__(self):
        pygame.init()

        self.menu_screen = screen.Screen()

        self.background = pygame.image.load('assets/background.png').convert_alpha()
        self.menu_font = pygame.font.Font('assets/game_font.ttf', 36)
        #  creates the three buttons for out main menu using the Button class
        self.play_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                         position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                   self.menu_screen.CELL_SIZE * 6],
                                         button_font=self.menu_font, base_color="White",
                                         highlight_color="Green", text_input="PLAY")
        self.options_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                            position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                      self.menu_screen.CELL_SIZE * 9],
                                            button_font=self.menu_font, base_color="White",
                                            highlight_color="Green", text_input="OPTIONS")
        self.quit_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                         position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                   self.menu_screen.CELL_SIZE * 12],
                                         button_font=self.menu_font, base_color="White",
                                         highlight_color="Green", text_input="QUIT")

        self.wall_game_mode = False
        self.no_walls_game_mode = False
        self.response_time = 150

        self.click_sound = pygame.mixer.Sound("assets/click.wav")
        self.play_sound = pygame.mixer.Sound("assets/play.wav")

# **********************************************************************************************************************

    def main_menu(self):
        title_font = pygame.font.Font('assets/game_font.ttf', 42)
        pygame.display.set_caption("Menu")
        self.menu_screen.display.blit(self.background, (0, 0))

        while True:
            menu_mouse_position = pygame.mouse.get_pos()
            menu_text = title_font.render("GARDEN OF EDEN", True, "Black")
            menu_rect = menu_text.get_rect(center=(self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                   self.menu_screen.CELL_SIZE * 3))

            self.menu_screen.display.blit(menu_text, menu_rect)

            # text changes color when highlighted by mouse
            for buttons in [self.play_button, self.options_button, self.quit_button]:
                buttons.highlight_color_change(menu_mouse_position)
                buttons.update(self.menu_screen.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_input(menu_mouse_position):
                        self.play_sound.play()
                        self.play_game()

                    if self.options_button.check_input(menu_mouse_position):
                        self.click_sound.play()
                        self.options_menu()

                    if self.quit_button.check_input(menu_mouse_position):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

# **********************************************************************************************************************

    def play_game(self):
        frame_rate = 60
        clock = pygame.time.Clock()

        background_music = pygame.mixer.Sound('assets/background_music.mp3')
        up_sound = pygame.mixer.Sound('assets/up_sound.wav')
        right_sound = pygame.mixer.Sound('assets/right_sound.wav')
        left_sound = pygame.mixer.Sound('assets/down_sound.wav')
        down_sound = pygame.mixer.Sound('assets/left_sound.wav')

        main_game = game.Game()

        main_game.set_response_time(self.response_time)
        pygame.display.set_caption("Play")

        if self.wall_game_mode == True:
            main_game.wall.set_game_mode_on()

        elif self.no_walls_game_mode == True:
            main_game.no_walls_game_mode = True

        background_music.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == main_game.SCREEN_UPDATE:
                    main_game.update()

                if main_game.is_high == False:  # normal gameplay i.e. user did not eat mushroom
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if main_game.snake.direction.y != 1:
                                main_game.snake.direction = Vector2(0, -1)
                                up_sound.play()

                        if event.key == pygame.K_RIGHT:
                            if main_game.snake.direction.x != -1:
                                main_game.snake.direction = Vector2(1, 0)
                                right_sound.play()

                        if event.key == pygame.K_DOWN:
                            if main_game.snake.direction.y != -1:
                                main_game.snake.direction = Vector2(0, 1)
                                down_sound.play()

                        if event.key == pygame.K_LEFT:
                            if main_game.snake.direction.x != 1:
                                main_game.snake.direction = Vector2(-1, 0)
                                left_sound.play()

                else:  # controls are flipped when user eats mushroom
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if main_game.snake.direction.y != -1:
                                main_game.snake.direction = Vector2(0, 1)
                                down_sound.play()

                        if event.key == pygame.K_RIGHT:
                            if main_game.snake.direction.x != 1:
                                main_game.snake.direction = Vector2(-1, 0)
                                left_sound.play()

                        if event.key == pygame.K_DOWN:
                            if main_game.snake.direction.y != 1:
                                main_game.snake.direction = Vector2(0, -1)
                                up_sound.play()

                        if event.key == pygame.K_LEFT:
                            if main_game.snake.direction.x != -1:
                                main_game.snake.direction = Vector2(1, 0)
                                right_sound.play()

            main_game.draw_elements()
            pygame.display.update()
            clock.tick(frame_rate)

# **********************************************************************************************************************

    def options_menu(self):
        options_font = pygame.font.Font('assets/game_font.ttf', 21)
        game_mode_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                         position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                   self.menu_screen.CELL_SIZE * 6],
                                         button_font=options_font, base_color="White",
                                         highlight_color="Green", text_input="GAME MODE")
        difficulty_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                          position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                    self.menu_screen.CELL_SIZE * 9],
                                          button_font=options_font, base_color="White",
                                          highlight_color="Green", text_input="DIFFICULTY")
        back_button = button.Button(button_image=pygame.image.load("assets/button.png"),
                                    position=[self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                              self.menu_screen.CELL_SIZE * 12],
                                    button_font=options_font, base_color="White",
                                    highlight_color="Green", text_input="BACK")

        game_mode_click_counter = 0
        difficulty_click_counter = 0

        pygame.display.set_caption("Options")
        self.menu_screen.display.blit(self.background, (0, 0))

        while True:
            options_menu_mouse_position = pygame.mouse.get_pos()
            options_menu_text = self.menu_font.render("OPTIONS", True, "Black")
            options_menu_rect = options_menu_text.get_rect(center=(self.menu_screen.CELL_SIZE * (self.menu_screen.CELL_NUMBER / 2),
                                                           self.menu_screen.CELL_SIZE * 3))

            self.menu_screen.display.blit(options_menu_text, options_menu_rect)

            # text changes color when highlighted by mouse
            for buttons in [game_mode_button, difficulty_button, back_button]:
                buttons.highlight_color_change(options_menu_mouse_position)
                buttons.update(self.menu_screen.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game_mode_button.check_input(options_menu_mouse_position):
                        game_mode_click_counter += 1
                        self.click_sound.play()

                        if(game_mode_click_counter % 3) == 1:
                            game_mode_button.text_input = "  NORMAL"
                            self.no_walls_game_mode = False

                        elif(game_mode_click_counter % 3) == 2:
                            game_mode_button.text_input = "  WALLS"
                            self.wall_game_mode = True

                        elif (game_mode_click_counter % 3) == 0:
                            game_mode_button.text_input = " NO WALLS"
                            self.wall_game_mode = False
                            self.no_walls_game_mode = True

                    if difficulty_button.check_input(options_menu_mouse_position):
                        difficulty_click_counter += 1
                        self.click_sound.play()

                        if (difficulty_click_counter % 3) == 1:
                            difficulty_button.text_input = "   EASY"
                            self.response_time = 150

                        elif (difficulty_click_counter % 3) == 2:
                            difficulty_button.text_input = "  MEDIUM"
                            self.response_time = 120

                        elif (difficulty_click_counter % 3) == 0:
                            difficulty_button.text_input = "   HARD"
                            self.response_time = 90

                    if back_button.check_input(options_menu_mouse_position):
                        self.click_sound.play()
                        self.main_menu()

            pygame.display.update()
