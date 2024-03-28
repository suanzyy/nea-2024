import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        # Initialize game properties
        self.max_level = 0
        self.max_health = 90
        self.cur_health = 90
        self.coins = 0

        # Load background music
        self.level_bg_music = pygame.mixer.Sound(r"D:\COMPUTER SCIENCE NEA 2024\tiled\audio\level_music.wav")
        self.overworld_bg_music = pygame.mixer.Sound(r"D:\COMPUTER SCIENCE NEA 2024\tiled\audio\overworld_music.wav")

        # Create the overworld and UI
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops=-1)
        self.ui = UI(screen)

    def create_level(self, current_level):
        # Create a new level
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        # Create a new overworld
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops=-1)

    def change_coins(self, amount):
        # Change the number of coins
        self.coins += amount

    def change_health(self, amount):
        # Change the player's health
        self.cur_health += amount

    def check_game_over(self):
        # Check if the game is over and reset if necessary
        if self.cur_health <= 0:
            self.cur_health = 90
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.overworld_bg_music.play(loops=-1)
            self.level_bg_music.stop()

    def run(self):
        # Run the game loop
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
        self.ui.show_health(self.cur_health, self.max_health)
        self.ui.show_coins(self.coins)
        self.check_game_over()

# Initialize Pygame and create the game instance
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()
    pygame.display.update()
    clock.tick(60)