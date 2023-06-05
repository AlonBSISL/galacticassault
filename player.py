import pygame
from settings import gravity
from bullet import Bullet
from support import import_folder
from enemy import Enemy


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        # self.image = pygame.Surface((32, 64))
        # self.image.fill("red")

        # Graphics
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.05

        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.jump_speed = -16
        self.status = "idle"

        self.shot_sound = pygame.mixer.Sound("sounds/effects/laser.mp3")
        self.bullets = pygame.sprite.Group()
        self.firing = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def import_character_assets(self):
        character_path = "graphics/player/"
        self.animations = {"idle": [], "right": [], "left": []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.x = 0

        # if keys[pygame.K_UP]:
        # self.jump()

        if keys[pygame.K_SPACE] and not self.firing:
            self.fire()
            self.firing = True
        elif not keys[pygame.K_SPACE] and self.firing:
            self.firing = False

    def fire(self):
        bullet = Bullet((self.rect.centerx, self.rect.centery), self.direction.y)
        self.shot_sound
        self.bullets.add(bullet)

    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        else:
            if self.direction.x == 0:
                self.status = "idle"
            else:
                self.status = "run"

    def jump(self):
        if self.status != "jump":
            self.status = "jump"
            self.direction.y = self.jump_speed

    def horizontal_movement_collision(self, tiles):
        self.rect.x += self.direction.x * self.speed
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                elif self.direction.x > 0:
                    self.rect.right = tile.rect.left

    def vertical_movement_collision(self, tiles):
        self.apply_gravity()

        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                if self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0

    def apply_gravity(self):
        self.direction.y += gravity
        self.rect.y += self.direction.y

    def update(self, tiles, enemies):
        self.get_input()
        self.horizontal_movement_collision(tiles)
        self.vertical_movement_collision(tiles)
        self.bullets.update()
        self.get_status()
        self.animate
        # self.get_status()
        # self.bullets.update()

    def draw_bullets(self, surface):
        self.bullets.draw(surface)
