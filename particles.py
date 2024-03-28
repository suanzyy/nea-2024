import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        # Initialize the ParticleEffect sprite
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        
        # Load the appropriate particle frames based on the type
        if type == 'jump':
            self.frames = import_folder('C:/Users/thanh/PycharmProjects/first python/graphics/character/dust_particles/jump')
        elif type == 'land':
            self.frames = import_folder('C:/Users/thanh/PycharmProjects/first python/graphics/character/dust_particles/land')
        elif type == 'explosion':
            self.frames = import_folder(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\enemy\explosion")
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        # Animate the particle effect
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  # Remove the particle effect when animation is done
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        # Update the particle effect
        self.animate()
        self.rect.x += x_shift  # Shift the particle effect horizontally