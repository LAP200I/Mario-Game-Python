import re

import pygame


class Text:
    def __init__(self, font, font_size, text, color, pos):
        self.font = font
        self.font_size = font_size
        self.text = text
        self.color = color
        self.anti_alias = True
        self.pos = pos
        self.onclick = None
        self.width = 0
        self.height = 0
        self.pressed = False

    def get_font(self):
        return pygame.font.Font(self.font, self.font_size)

    def get_display_text(self):
        return self.text

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        text_rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.width, self.height)
        if text_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.onclick()
                    self.pressed = False
        else:
            pass

    def render(self, screen):
        text_surface = self.get_font().render(self.get_display_text(), self.anti_alias, self.color)
        self.width = text_surface.get_width()
        self.height = text_surface.get_height()
        screen.blit(text_surface, self.pos)
        if self.onclick is not None:
            self.check_click()

    def set_on_click(self, onclick):
        self.onclick = onclick


class Input(Text):
    def __init__(self, font, font_size, color, rect, border_width, border_active_color, border_inactive_color,
                 max_char=24, reg=".", input_formatter=None):
        super().__init__(font, font_size, "", color, (rect.x + 5, rect.y + rect.height / 2 - font_size / 2 + 5))
        self.rect = rect
        self.border_width = border_width
        self.border_active_color = border_active_color
        self.border_inactive_color = border_inactive_color
        self.active = False
        self.max_char = max_char
        self.reg = reg
        self.input_formatter = input_formatter
        self.display_text = ""

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.display_text = self.display_text[:-1]
                else:
                    if len(self.text) <= self.max_char:
                        m = re.search(self.reg, event.unicode)
                        if m is not None:
                            new_char = event.unicode
                            if self.input_formatter is not None:
                                display_char = self.input_formatter(event.unicode)
                                self.display_text += display_char
                            self.text += new_char

    def get_display_text(self):
        if self.input_formatter is None:
            return self.text
        return self.display_text

    def render(self, screen):
        super().render(screen)
        if self.active:
            color = self.border_active_color
        else:
            color = self.border_inactive_color
        pygame.draw.rect(screen, color, self.rect, self.border_width)


class Button:
    def __init__(self, text, rect, elevation, onclick=None):
        # core attribute
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = rect.y

        # top rectangle
        self.top_rect = rect
        self.top_color = "#475F77"

        # bottom_rect
        self.bottom_rect = pygame.Rect((rect.x, rect.y), (rect.width, elevation))
        self.bottom_color = "#354B5E"

        # text
        gui_font = pygame.font.Font(None, 30)
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self.onclick = onclick

    def render(self, display_surface):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(display_surface, self.bottom_color, self.bottom_rect, border_radius=20)
        pygame.draw.rect(display_surface, self.top_color, self.top_rect, border_radius=20)
        display_surface.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed:
                    if self.onclick is not None:
                        self.onclick()
                    self.pressed = False
                    self.dynamic_elevation = self.elevation
        else:
            self.top_color = "#475F77"
            self.dynamic_elevation = self.elevation
