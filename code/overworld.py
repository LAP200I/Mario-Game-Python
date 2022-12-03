import pygame.sprite

from decoration import Sky
from game_data import levels
from settings import *
from support import import_folder
from view import Text, Button


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(
            self.rect.centerx - icon_speed / 2,
            self.rect.centery
            - icon_speed / 2,
            icon_speed, icon_speed
        )

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, is_enable, username, do_log_out):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.moving = False

        # sprites
        self.nodes = pygame.sprite.Group()
        self.setup_nodes()
        self.icon = pygame.sprite.GroupSingle()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

        self.is_enable = is_enable

        self.text_color = (255, 255, 255)
        self.user_name = username
        self.user_name_label = Text(None, 32, self.user_name, self.text_color,
                                    (0, 20))

        self.login_button_rect = pygame.Rect(screen_width - 160, 60, 150, 50)
        self.login_button = Button("Logout", self.login_button_rect, 6, onclick=self.logout)
        self.do_log_out = do_log_out

    def logout(self):
        self.do_log_out()

    def setup_icon(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def setup_nodes(self):
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [
                node['node_pos']
                for index, node
                in enumerate(levels.values())
                if index <= self.max_level
            ]
            pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def input(self):
        if not self.is_enable:
            return
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level != self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level != 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_RETURN]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        pos = self.current_level + 1
        if target == 'previous':
            pos = self.current_level - 1
        end = pygame.math.Vector2(self.nodes.sprites()[pos].rect.center)
        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.input()
        self.sky.draw(self.display_surface)
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        if self.is_enable:
            self.user_name_label.render(self.display_surface)
            self.user_name_label.pos = (screen_width - self.user_name_label.width - 20, self.user_name_label.pos[1])
            self.login_button.render(self.display_surface)
