import sys
import pygame
from pygame.locals import *

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 725, 725
screen = pygame.display.set_mode((width, height))


class Slippers(pygame.sprite.Sprite):
    pass


class Floor(pygame.sprite.Sprite):
    pass


class Cleaner(pygame.sprite.Sprite):
    pass


class Puddle(pygame.sprite.Sprite):
    pass


class Cockroach(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.image.load('cocroach.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (145, 150))

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 435


all_sprites = pygame.sprite.Group()
Cockroach(all_sprites)

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update

    # Draw
    all_sprites.draw(screen)
    pygame.display.flip()

    fpsClock.tick(fps)
