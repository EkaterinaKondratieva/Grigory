import sys
import pygame
from pygame.locals import *
import random


class Cleaner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.time = pygame.time.get_ticks()
        self.start = random.choice([2,1,3]) * 1000
        self.image = pygame.image.load('cleaner.jpeg')
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topright = (self.x, self.y)

    def move(self):
        if pygame.time.get_ticks() - self.time >= self.start:
            self.rect.x += 1


class Puddle(pygame.sprite.Sprite):
    pass


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
    for i in range(3):
        num = random.choice([1, 2, 3])
        # 1 cleaner
        # 2 puddle
        # 3 slipers
        print(num)
        if num == 3:
            Slipers(0, 145 * i)
        elif num == 1:
            cleaners.append(Cleaner(0, 145 * i))

        # else:
        #     Puddle(0, 145 * i)


pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 725, 725
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()
cleaners = []
fon = pygame.image.load('floor.jpg')
fon = pygame.transform.scale(fon, (725, 725))
screen.blit(fon, (0, 0))
start_fon()
Cockroach(all_sprites)

while True:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update
    for elem in cleaners:
        elem.move()

    # Draw
    all_sprites.draw(screen)

    pygame.display.flip()
    fpsClock.tick(fps)
