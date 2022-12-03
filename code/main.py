import os
import sys

import pygame

from account_controller import AccountController
from connector import set_up_db
from game_data_controller import GameDataController
from level import Level
from login import LoginScreen
from overworld import Overworld
from settings import *
from ui import UI


class Game:
    def __init__(self):
        self.game_data_controller = GameDataController()
        self.account_controller = AccountController()

        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
        self.over_world_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')

        # login
        self.is_login = False
        self.login_screen = LoginScreen(screen, self.do_login_success)
        # overworld creation
        self.username = ""
        self.over_world = Overworld(0, self.max_level, screen, self.create_level, self.is_login, self.username,
                                    self.do_log_out)
        self.status = 'overworld'
        self.over_world_bg_music.play(loops=-1)

        # user interface
        self.ui = UI(screen)

        self.check_cache_login()

    def check_cache_login(self):
        user_name = self.account_controller.check_cache_login()
        if user_name is not None:
            self.do_login_success(user_name)

    def do_log_out(self):
        self.is_login = False
        self.username = ""
        self.over_world.is_enable = False
        os.remove('../account.txt')

    def do_login_success(self, username):
        self.is_login = True
        self.username = username
        game_data = self.game_data_controller.get_game_data(username)
        self.coins = game_data[1]
        self.max_level = game_data[2]
        self.create_overworld(0, self.max_level)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.over_world_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
            self.game_data_controller.update_next_level(self.username, new_max_level)
        self.over_world = Overworld(current_level, self.max_level, screen, self.create_level, self.is_login,
                                    self.username, self.do_log_out)
        self.status = 'overworld'
        self.reset_game_data()
        self.level_bg_music.stop()
        self.over_world_bg_music.stop()
        self.over_world_bg_music.play(loops=-1)

    def change_coins(self, amount):
        self.coins += amount
        self.game_data_controller.update_coin(self.username, self.coins)

    def change_health(self, amount):
        self.current_health += amount

    def reset_game_data(self):
        self.current_health = 100

    def check_game_over(self):
        if self.current_health < 0:
            self.create_overworld(self.over_world.current_level, self.max_level)
            self.change_coins(-10)

    def run(self):
        if self.status == 'overworld':
            self.over_world.run()
            if not self.is_login:
                self.login_screen.draw(screen)
            else:
                self.ui.show_coins(self.coins)

        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


set_up_db()
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        game.login_screen.update(event)

    screen.fill('grey')
    game.run()
    pygame.display.update()
    clock.tick(60)
