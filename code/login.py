from account_controller import AccountController
from game_data_controller import GameDataController
from settings import *
from view import *


class LoginScreen:
    def __init__(self, display_surface, do_login_success):
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.text_color = (255, 255, 255)
        self.display_surface = display_surface
        self.do_login_success = do_login_success
        self.state = 'login'

        self.account_controller = AccountController()
        self.game_data_controller = GameDataController()

        self.user_name_rect = pygame.Rect(screen_width / 2 - 250, screen_height / 2 - 100, 500, 32)
        self.user_name_label = Text(None, 32, "User name:", self.text_color,
                                    (self.user_name_rect.x - 155, self.user_name_rect.y + 5))
        self.user_name_input = Input(None, 32, self.text_color, self.user_name_rect, 2, self.color_active,
                                     self.color_passive, reg='[\\w]')

        self.password_rect = pygame.Rect(self.user_name_rect.x, self.user_name_rect.y + self.user_name_rect.height + 20,
                                         self.user_name_rect.width,
                                         self.user_name_rect.height)
        self.password_label = Text(None, 32, "Password:", self.text_color,
                                   (self.password_rect.x - 140, self.password_rect.y + 5))
        self.password_input = Input(None, 32, self.text_color, self.password_rect, 2, self.color_active,
                                    self.color_passive, reg='[\\w]',
                                    input_formatter=lambda k: "*")

        self.confirm_password_rect = pygame.Rect(self.password_rect.x,
                                                 self.password_rect.y + self.password_rect.height + 20,
                                                 self.password_rect.width,
                                                 self.password_rect.height)
        self.confirm_password_label = Text(None, 32, "Confirm Password:", self.text_color,
                                           (self.confirm_password_rect.x - 230, self.confirm_password_rect.y + 5))
        self.confirm_password_input = Input(None, 32, self.text_color, self.confirm_password_rect, 2, self.color_active,
                                            self.color_passive, reg='[\\w]',
                                            input_formatter=lambda k: "*")

        self.login_button_rect = pygame.Rect(self.password_rect.x,
                                             self.password_rect.y + self.password_rect.height + 20,
                                             self.password_rect.width, 50)

        self.login_button = Button("Login", self.login_button_rect, 6, onclick=self.login)

        self.register_label = Text(None, 32, "Don't have account? Register!", self.text_color,
                                   (self.password_rect.x + 80,
                                    self.login_button_rect.y + self.login_button_rect.height + 20))
        self.register_label.set_on_click(self.to_register)

        self.register_button_rect = pygame.Rect(self.password_rect.x,
                                                self.confirm_password_rect.y + self.confirm_password_rect.height + 20,
                                                self.confirm_password_rect.width, 50)
        self.register_button = Button("Register", self.register_button_rect, 6, onclick=self.register)

        self.login_label = Text(None, 32, "Already have account? Login!", self.text_color,
                                (self.password_rect.x + 80,
                                 self.register_button_rect.y + self.register_button_rect.height + 20))
        self.login_label.set_on_click(self.to_login)

        self.errorText = Text(None, 32, "", 'red',
                              (self.password_rect.x + 50,
                               self.register_button_rect.y + self.register_button_rect.height + 70))

    def to_register(self):
        self.state = "register"
        self.errorText.text = ""

    def to_login(self):
        self.state = "login"
        self.errorText.text = ""

    def login(self):
        user_name = self.user_name_input.text
        password = self.password_input.text
        if len(user_name) < 6:
            self.errorText.text = "Username must have at least 6 characters"
            return
        if len(password) < 6:
            self.errorText.text = "Password must have at least 6 characters"
            return
        rs = self.account_controller.login(user_name, password)
        if rs is None:
            self.errorText.text = ""
            self.do_login_success(user_name)
        else:
            self.errorText.text = rs

    def register(self):
        user_name = self.user_name_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if len(user_name) < 6:
            self.errorText.text = "Username must have at least 6 characters"
            return
        if len(password) < 6:
            self.errorText.text = "Password must have at least 6 characters"
            return
        if confirm_password != password:
            self.errorText.text = "Confirm password not match"
            return
        else:
            self.errorText.text = ""
        rs = self.account_controller.register(self.user_name_input.text, self.password_input.text)
        if rs is None:
            self.game_data_controller.create_game_data(user_name)
            self.to_login()
        else:
            self.errorText.text = rs

    def update(self, event):
        self.user_name_input.update(event)
        self.password_input.update(event)
        self.confirm_password_input.update(event)

    def draw(self, display_surface):
        self.user_name_label.render(display_surface)
        self.user_name_input.render(display_surface)

        self.password_label.render(display_surface)
        self.password_input.render(display_surface)

        if self.state == "login":
            self.login_button.render(display_surface)
            self.register_label.render(display_surface)

        if self.state == 'register':
            self.confirm_password_label.render(display_surface)
            self.confirm_password_input.render(display_surface)
            self.register_button.render(display_surface)
            self.login_label.render(display_surface)

        self.errorText.render(display_surface)
        self.errorText.pos = (screen_width / 2 - self.errorText.width / 2, self.errorText.pos[1])
