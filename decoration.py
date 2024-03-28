import pygame
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

# Define a class for rendering the sky background
class Sky:
    def __init__(self, horizon, style='level'):
        # Load sky images for different parts
        self.top = pygame.image.load(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\decoration\sky\sky_top.png").convert()
        self.bottom = pygame.image.load(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\decoration\sky\sky_bottom.png").convert()
        self.middle = pygame.image.load(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\decoration\sky\sky_middle.png").convert()
        self.horizon = horizon

        # Scale the sky images to fit the screen
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

        self.style = style

        # If the style is 'overworld', load additional elements like palms and clouds
        if self.style == 'overworld':
            # Load palm tree images
            palm_surfaces = import_folder(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\overworld\palms")
            self.palms = []

            # Create palm tree instances with random positions
            for surface in [choice(palm_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.palms.append((surface, rect))

            # Load cloud images
            cloud_surfaces = import_folder(r"D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\overworld\clouds")
            self.cloud = []

            # Create cloud instances with random positions
            for surface in [choice(cloud_surfaces) for image in range(10)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * tile_size) - 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.cloud.append((surface, rect))

    # Method to draw the sky on the given surface
    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        # If the style is 'overworld', draw additional elements like palms and clouds
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.cloud:
                surface.blit(cloud[0], cloud[1])

# Define a class for rendering water elements
class Water:
    def __init__(self, top, level_width):
        # Initialize water parameters
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprite = pygame.sprite.Group()

        # Create water tiles and add them to a sprite group
        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, r'D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\decoration\water')
            self.water_sprite.add(sprite)

    # Method to draw water on the given surface with a shift
    def draw(self, surface, shift):
        self.water_sprite.update(shift)
        self.water_sprite.draw(surface)

# Define a class for rendering cloud elements
class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        # Load cloud images
        cloud_surf_list = import_folder(r'D:\COMPUTER SCIENCE NEA 2024\tiled\graphics\decoration\clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        # Create cloud instances with random positions and add them to a sprite group
        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    # Method to draw clouds on the given surface with a shift
    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
