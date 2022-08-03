import pygame

# **********************************************************************************************************************

class Button():
    pygame.init()

    def __init__(self, button_image, position, button_font, base_color, highlight_color, text_input):
        self.button_image = button_image
        self.x_position = position[0]
        self.y_position = position[1]
        self.button_font = button_font
        self.base_color = base_color
        self.highlight_color = highlight_color
        self.text_input = text_input
        self.text = self.button_font.render(self.text_input, True, self.base_color)

        if self.button_image is None:
            self.button_image = self.text

        self.button_rect = self.button_image.get_rect(center=(self.x_position, self.y_position))
        self.text_rect = self.text.get_rect(center=(self.x_position, self.y_position))

# **********************************************************************************************************************

    def update(self, screen):
        if self.button_image is not None:
            screen.blit(self.button_image, self.button_rect)

        screen.blit(self.text, self.text_rect)

# **********************************************************************************************************************

    def check_input(self, position):
        # check if the user's mouse is within the button
        if position[0] in range(self.button_rect.left, self.button_rect.right) \
                and position[1] in range(self.button_rect.top, self.button_rect.bottom):
            return True

        return False

# **********************************************************************************************************************

    def highlight_color_change(self, position):
        if position[0] in range(self.button_rect.left, self.button_rect.right) \
                and position[1] in range(self.button_rect.top, self.button_rect.bottom):
            self.text = self.button_font.render(self.text_input, True, self.highlight_color)

        else:
            self.text = self.button_font.render(self.text_input, True, self.base_color)
