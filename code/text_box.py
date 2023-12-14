import pygame
from settings import *

class Text_Box:
    def __init__(self, text, toggle_text_box):
        self.text = text
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.width = WIDTH - 2 * TEXTBOX_SIDE_OFFSET
        self.height = TEXTBOX_HEIGHT
        self.surface = pygame.Surface((self.width, self.height)).convert_alpha()
        self.surface.fill(TEXTBOX_BG_COLOR)
        self.rect = self.surface.get_rect(topleft = (TEXTBOX_SIDE_OFFSET, HEIGHT - TEXTBOX_BOTTOM_OFFSET - self.height))

        self.max_text_width = self.width - 2 * TEXT_OFFSET

        #self.text_surf = self.font.render(self.text, True, TEXT_COLOR)
        #self.text_rect = self.text_surf.get_rect(topleft = (TEXTBOX_SIDE_OFFSET,TEXTBOX_SIDE_OFFSET))

        self.input_time = None
        self.can_input = True
        self.input_cooldown = 150

        self.index = 0
        self.state = "autofill" # Autofill or idle
        self.autofill_text = ""
        self.autofill_index = 0
        self.view_index = 0

        self.toggle_text_box = toggle_text_box

        self.create_text_surfaces()

    def create_text_surfaces(self):
        self.text_data = []
        current_text = ""
        previous_text = ""
        index = 0
        for word in self.text.split(" "):
            next_word = False
            while not next_word:
                current_text = word if current_text == "" else f'{current_text} {word}'
                text_surf = self.font.render(current_text, True, TEXT_COLOR)
                if text_surf.get_width() > self.max_text_width:
                    if previous_text == "":
                        raise ValueError(f'Word \'{word}\' is too big, consider decreasing font size')
                    else:
                        self.text_data.append(self.add_text_data(previous_text, index))
                        previous_text = ""
                        current_text = ""
                        index += 1
                else:
                    previous_text = current_text
                    next_word = True
        if not current_text == "":
            self.text_data.append(self.add_text_data(current_text, index))

    def add_text_data(self, text, index):
        text_surf = self.font.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(topleft = (TEXT_OFFSET, TEXT_OFFSET + TEXT_VERTICAL_DISTANCE * index))
        return (text, text_surf, text_rect, index)

    def input(self):
        if self.can_input:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RETURN]:
                if self.state == "autofill":
                    self.index = self.view_index + TEXT_LINES_NUM
                    self.state = "idle"
                    self.autofill_text = ""
                    self.autofill_index = 0
                    if self.index > len(self.text_data) - 1:
                        self.state = "end"
                elif self.state == "idle":
                    self.move_text()
                elif self.state == "end":
                    self.state = "over"
                    self.toggle_text_box()
                    self.restart()

                self.input_time = pygame.time.get_ticks()
                self.can_input = False


    def move_text(self):
        for text_data in self.text_data:
            text_data[2].y -= TEXT_VERTICAL_DISTANCE * TEXT_LINES_NUM
        self.view_index += TEXT_LINES_NUM
        self.state = "autofill"

    def cooldown(self):
        if not self.can_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.input_time > self.input_cooldown:
                self.can_input = True
                self.input_time = None

    def restart(self):
        self.index = 0
        self.state = "autofill" # Autofill or idle
        self.autofill_text = ""
        self.autofill_index = 0
        self.view_index = 0

    def autofill(self):
        goal_text = self.text_data[self.index][0]
        self.autofill_text += goal_text[self.autofill_index]
        self.autofill_index += 1
        if self.autofill_text == goal_text:
            self.index += 1
            self.autofill_text = ""
            self.autofill_index = 0
            if self.index > self.view_index + TEXT_LINES_NUM - 1:
                self.state = 'idle'
            if self.index > len(self.text_data) - 1:
                self.state = "end"

    def display(self, surface):
        self.surface.fill(TEXTBOX_BG_COLOR)
        if self.state == "autofill":
            self.autofill()

        for text_data in self.text_data:
            if text_data[3] < self.view_index:
                pass
            elif text_data[3] < self.index:
                self.surface.blit(text_data[1], text_data[2])
            elif text_data[3] == self.index:
                    text_surf = self.font.render(self.autofill_text, True, TEXT_COLOR)
                    self.surface.blit(text_surf, text_data[2])

        surface.blit(self.surface, self.rect)
        pygame.draw.rect(surface, TEXTBOX_BORDER_COLOR, self.rect, 2)

    def update(self, surface):
        self.input()
        self.cooldown()
        if not self.state == "over":
            self.display(surface)
