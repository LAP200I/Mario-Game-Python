from math import sin

import pygame

from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.import_assets()

        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particles = create_jump_particles

        self.display_surface = surface
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.gravity = 1
        self.jump_speed = -22
        self.status = 'idle'
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        self.on_ground = True
        self.facing_right = True

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

    def import_assets(self):
        character_path = '../graphics/character/'
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        img = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = img
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_img = pygame.transform.flip(img, True, False)
            self.image = flipped_img
            self.rect.bottomright = self.collision_rect.bottomright
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0:
            self.status = 'fall'
        elif self.direction.x == 0:
            self.status = 'idle'
        else:
            self.status = 'run'

    def on_key_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.jump_sound.play()
        self.direction.y = self.jump_speed
        self.create_jump_particles(self.collision_rect.midbottom)

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time > self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.on_key_event()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
