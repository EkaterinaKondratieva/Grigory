import sys
import pygame
from pygame.locals import *
import random


class Cleaner(pygame.sprite.Sprite):
    # def __init__(self, x, y):
    #
    #
    # def update(self):
    #     self.rect.y += 145
    pass


class Puddle(pygame.sprite.Sprite):
    pass


class Slipers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('carpet.jpg')
        self.image = pygame.transform.scale(self.image, (725, 145))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.y += 145


class Cockroach(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.image.load('cocroach.gif').convert_alpha()
        self.image = pygame.transform.scale(self.image, (145, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 435


def start_fon():
    fon = pygame.image.load('floor.jpg')
    fon = pygame.transform.scale(fon, (725, 725))
    screen.blit(fon, (0, 0))
    for i in range(4):
        num = random.choice([1, 2, 3])
        if num == 3:
            Slipers(0, 145 * i)


pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 725, 725
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()
start_fon()
Cockroach(all_sprites)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    all_sprites.update()
    # Draw
    all_sprites.draw(screen)
    pygame.display.flip()
    fpsClock.tick(fps)
