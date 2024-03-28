import pygame
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        # Initialize the Player sprite
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Dust particles for running animation
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Player health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 800
        self.hurt_time = 0

        # Sound effects
        self.jump_sound = pygame.mixer.Sound(r"D:\COMPUTER SCIENCE NEA 2024\tiled\audio\effects\mario jump sfx.mp3")
        self.hit_sound = pygame.mixer.Sound(r"D:\COMPUTER SCIENCE NEA 2024\tiled\audio\effects\steve oof sfx.mp3")

    def import_character_assets(self):
        # Load the character animation sprites
        character_path = 'C:/Users/thanh/PycharmProjects/first python/graphics/character/'
        self.animations = {'fall': [], 'idle': [], 'run': [], 'jump': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        # Load the dust particle sprites for running animation
        self.dust_run_particles = import_folder('C:/Users/thanh/PycharmProjects/first python/graphics/character/dust_particles/run')

    def animate(self):
        # Handle character animation based on current status
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            # Make the player sprite blink when invincible
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def run_dust_animation(self):
        # Display dust particles when running on the ground
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

    def get_input(self):
        # Handle player input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        # Update player status based on movement
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        # Apply gravity to the player
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        # Make the player jump and play a sound effect
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        # Handle player getting damaged
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-30)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        # Handle player invincibility duration
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        # Helper function for blinking effect when invincible
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        # Update the player state
        self.get_input()
        self.animate()
        self.get_status()
        self.run_dust_animation()
        self.invincibility_timer()