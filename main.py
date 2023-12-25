import sys
import pygame
from pygame.locals import *
import random


class Cleaner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.cleaner = pygame.image.load('cleaner.jpeg')
        self.cleaner = pygame.transform.scale(self.cleaner, (100, 100))



class Puddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)


class Slipers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('carpet.jpeg')
        self.image = pygame.transform.scale(self.image, (725, 145))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 145


class Cockroach(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.image.load('cockroach.jpeg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (145, 150))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 435


def start_fon():
    fon = pygame.image.load('floor.jpg')
    fon = pygame.transform.scale(fon, (725, 725))
    screen.blit(fon, (0, 0))
    for i in range(3):
        num = random.choice([1, 2, 3])
        # 1 cleaner
        # 2 puddle
        # 3 slipers
        if num == 3:
            Slipers(0, 145 * i)
        # elif num == 1:
        #     Cleaner(0, 145 * i)
        # else:
        #     Puddle(0, 145 * i)


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

    # Draw
    all_sprites.draw(screen)
    pygame.display.flip()
    fpsClock.tick(fps)
