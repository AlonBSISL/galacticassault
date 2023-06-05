import pygame
import random
from enemy import Enemy
from player import Player
from settings import *
from tile import Tile
from bullet import Bullet


def player_die():
    # Add your code here to handle player death
    # For example, decrease lives or end the game
    print("You lost")
    pygame.QUIT


class Level:

    def __init__(self, level_data, surface):

        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()  # Add a group for enemy projectiles
        self.setup_level(level_data)

    def setup_level(self, layout):

        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == "p":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
        for i in range(10):
            enemy = Enemy((random.randint(500, screen_width), random.randint(400, screen_height)))
            self.enemies.add(enemy)

    def check_bullet_collisions(self):
        pygame.sprite.groupcollide(self.player.sprite.bullets, self.enemies, False, True)

        # Check collision between enemy projectiles and player
        collided_with = pygame.sprite.spritecollide(self.player.sprite, self.enemy_projectiles, True)
        if collided_with:
            # Handle player death here (e.g., decrease lives, end game, etc.)
            player_die()

    def run(self):
        self.tiles.draw(self.display_surface)
        self.player.update(self.tiles, self.enemies)
        self.enemies.update()
        self.player.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        collided_with = pygame.sprite.spritecollide(self.player.sprite, self.enemies, True)

        self.player.sprite.draw_bullets(self.display_surface)
        self.enemy_projectiles.update()  # Update enemy projectiles
        self.enemy_projectiles.draw(self.display_surface)  # Draw enemy projectiles

        self.check_bullet_collisions()
