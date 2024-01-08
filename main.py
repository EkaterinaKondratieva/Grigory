import sys
import pygame
from pygame.locals import *
import random


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('floor.jpg')
        self.image = pygame.transform.scale(self.image, (750, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y


class Cleaner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.time = pygame.time.get_ticks()
        self.start = random.choice([0, 2, 1, 3]) * 1000
        self.image = pygame.image.load('cleaner.png')
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (-75, self.y + 75)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if pygame.time.get_ticks() - self.time >= self.start:
            self.rect.x += 3


class Puddle(pygame.sprite.Sprite):
    pass


class Carpet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('carpet.jpeg')
        self.image = pygame.transform.scale(self.image, (750, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y


class Slipers(pygame.sprite.Sprite):
    pass


class Cockroach(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load('cockroach.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (146, 140))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.rect.topleft = (302, 455)
        self.x = 302
        self.y = 455
        self.mask = pygame.mask.from_surface(self.image)

    def get_image(self):
        return self.image

    def move(self):
        self.rect.y -= 150

    def colllision(self):
        game_over = False
        for elem in cleaners:
            if pygame.sprite.collide_mask(self, elem):
                game_over = True
                break
        return game_over


def start_fon():
    for i in range(3):
        num = random.choice([1, 2, 3])
        # 1 cleaner
        # 2 puddle
        # 3 slipers
        print(num)
        if num == 3:
            Carpet(0, 150 * i)
            # Slipers(0, 150 * i)
        elif num == 1:
            Floor(0, 150 * i)
            cleaners.append(Cleaner(0, 150 * i))
        # else:
        #     Puddle(0, 145 * i)
        Floor(0, 150 * 3)
        Floor(0, 150 * 4)


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
        self.dy = -(target.rect.y + target.rect.h // 2 - height / 5 * 3 - 75)


pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()

cleaners = []

start_fon()

cockroach = Cockroach()

camera = Camera()

score = 0
game = True
next_wind = True
while next_wind:
    pygame.display.update()
    while game:
        screen.fill('white')
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
                    Carpet(0, -150)
                    # Slipers(0, -150)
                elif num == 1:
                    Floor(0, -150)
                    cleaners.append(Cleaner(0, -150))
                # else:
                #     Puddle(0, -145)

        # Update
        for elem in cleaners:
            elem.move()

        camera.update(cockroach)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        if cockroach.colllision():
            game = False
        else:
            score += 1
        # Draw
        all_sprites.draw(screen)
        screen.blit(cockroach.get_image(), (cockroach.x, cockroach.y))
        pygame.display.flip()
        fpsClock.tick(fps)

    width, height = 450, 450
    screen = pygame.display.set_mode((width, height))

    fon = pygame.image.load('floor.jpg')
    fon = pygame.transform.scale(fon, (450, 450))
    screen.blit(fon, (0, 0))

    restart = pygame.image.load('restart.png').convert_alpha()
    restart = pygame.transform.scale(restart, (144, 144))
    screen.blit(restart, (153, 225))
    for event in pygame.event.get():
        if event.type == QUIT:
            next_wind = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            x_pos = pos[0]
            y_pos = pos[1]
            if 297 >= x_pos and x_pos >= 153 and y_pos >= 225 and y_pos <= 369:
                print('ckicked')
                game = True
                width, height = 750, 750
                screen = pygame.display.set_mode((width, height))
                screen.fill('white')
                cleaners = []
                start_fon()
    pygame.display.flip()
    fpsClock.tick(fps)
