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
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (-75, self.y + 75)
    def move(self):
        if pygame.time.get_ticks() - self.time >= self.start:
            self.rect.x += 2


class Puddle(pygame.sprite.Sprite):
    pass


class Slipers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('carpet.jpeg')
        self.image = pygame.transform.scale(self.image, (750, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y


class Cockroach(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('cockroach.jpeg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (146, 140))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.topleft = (302, 455)
        self.x = 302
        self.y = 455

    def get_image(self):
        return self.image

    def move(self):
        self.rect.y -= 150



def start_fon():
    for i in range(3):
        num = random.choice([1, 2, 3])
        # 1 cleaner
        # 2 puddle
        # 3 slipers
        print(num)
        if num == 3:
            Slipers(0, 150 * i)
        elif num == 1:
            cleaners.append(Cleaner(0, 150 * i))

        # else:
        #     Puddle(0, 145 * i)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = 0
        self.dy = -(target.rect.y + target.rect.h // 2 - height / 5 * 3 - 60)


pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()

cleaners = []

fon = pygame.image.load('floor.jpg')
fon = pygame.transform.scale(fon, (750, 750))
screen.blit(fon, (0, 0))
start_fon()

cockroach = Cockroach()

camera = Camera()


while True:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            cockroach.move()
            num = random.choice([1, 2, 3])
            # 1 cleaner
            # 2 puddle
            # 3 slipers

            if num == 3:
                Slipers(0, -145)
            elif num == 1:
                cleaners.append(Cleaner(0, -145))
            # else:
            #     Puddle(0, -145)


    # Update
    for elem in cleaners:
        elem.move()

    camera.update(cockroach)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)


    # Draw
    all_sprites.draw(screen)
    screen.blit(cockroach.get_image(), (cockroach.x, cockroach.y - 17 ))
    pygame.display.flip()
    fpsClock.tick(fps)
