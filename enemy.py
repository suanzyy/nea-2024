import pygame
from tiles import AnimatedTile  # Import AnimatedTile class for inheritance
from random import randint

# Define a class for enemies, inheriting from AnimatedTile
class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        # Call the constructor of the parent class (AnimatedTile)
        super().__init__(size, x, y, r'D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\enemy\run')

        # Adjust the position of the enemy's rectangle to align it with the bottom of the image
        self.rect.y += size - self.image.get_size()[1]

        # Set a random speed for the enemy
        self.speed = randint(3, 5)

    # Method to move the enemy horizontally
    def move(self):
        self.rect.x += self.speed

    # Method to reverse the image of the enemy
    def reverse_image(self):
        # If the enemy is moving to the right, flip the image horizontally to face left
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    # Method to reverse the direction of the enemy's movement
    def reverse(self):
        self.speed *= -1

    # Method to update the enemy's position and animation
    def update(self, shift):
        # Shift the enemy's position based on the level scrolling
        self.rect.x += shift

        # Update the animation of the enemy
        self.animate()

        # Move the enemy horizontally
        self.move()

        # Reverse the image of the enemy if needed
        self.reverse_image()
