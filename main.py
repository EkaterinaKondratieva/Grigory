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
        self.сleaners_in_line = []
        self.time = pygame.time.get_ticks()
        self.start = random.choice([0, 2, 1, 3]) * 1000
        self.image = pygame.sprite.Sprite()
        self.image = pygame.image.load('cleaner.jpeg')
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (-75, self.y + 75)
        self.mask = pygame.mask.from_surface(self.image)
        # Polina is very very angry, she is scaring me. Help us please, we don't wanna die...I mean, we do, but noooo
        self.сleaners_in_line.append(self.image)
        self.next_cleaner = random.choice([2, 3, 4]) * 1000

    def move(self):
        self.rect.x += 3

    def new_cleaner(self):
        # print('new_cleaner')
        new = pygame.image.load('cleaner.jpeg')
        new = pygame.transform.scale(new, (160, 160))
        new.set_colorkey('white')
        new_rect = new.get_rect()
        top_right = (self.x, self.y)
        self.сleaners_in_line.insert(0, new)


class Puddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.image.load('puddle.png')
        self.image.set_colorkey('white')
        self.image = pygame.transform.scale(self.image, (750, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y


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
        self.rect = self.image.get_rect()
        self.pixel_rect = self.image.get_bounding_rect()
        self.trimmed_surface = pygame.Surface(self.pixel_rect.size)
        self.trimmed_surface.blit(self.image, (0, 0), self.pixel_rect)
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
        else:
            Floor(0, 150 * i)
            Puddle(0, 145 * i)
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


def restart():
    pygame.draw.rect(screen, 'white', ((150, 150), (450, 450)), width=0)
    pygame.draw.rect(screen, 'black', ((145, 145), (455, 455)), width=5)


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

pygame.font.init()
font = pygame.font.SysFont('comicsansms', 35)

score = 0

all_results = []
game = True
next_wind = True
while next_wind:
    while game:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                cockroach.move()
                score += 1
                num = random.choice([1, 2, 3, 4])
                # 1 cleaner
                # 2 puddle
                # 3 slipers
                # 4 floor
                if num == 1:
                    Floor(0, -150)
                    cleaners.append(Cleaner(0, -150))
                elif num == 2:
                    Floor(0, -150)
                    Carpet(0, -150)
                elif num == 3:
                    Carpet(0, -150)
                    # Slipers(0, -150)
                elif num == 1:
                    Floor(0, -150)
                    cleaners.append(Cleaner(0, -150))
                elif num == 4:
                    Floor(0, -150)

        # Update
        for elem in cleaners:
            elem.move()

        camera.update(cockroach)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        if cockroach.colllision():
            game = False
            all_results.append(score)

        # Draw
        all_sprites.draw(screen)
        screen.blit(cockroach.get_image(), (cockroach.x, cockroach.y))
        text = font.render(str(score), True, (255, 0, 0))
        text = font.render(f'{str(score)}', True, (255, 0, 0))
        screen.blit(text, (375, 0))
        pygame.display.flip()
        fpsClock.tick(fps)

    #######
    restart()
    restart_button = pygame.image.load('restart.png').convert_alpha()
    restart_button = pygame.transform.scale(restart_button, (144, 144))
    screen.blit(restart_button, (303, 375))

    font = pygame.font.SysFont('comicsansms', 35)

    text = font.render(f'Ваш результат: {str(score)}', True, (0, 0, 0))
    screen.blit(text, (150 + 80, 350 - 110))
    #
    text2 = font.render(f'Лучший результат: {str(max(all_results))}', True, (0, 0, 0))
    screen.blit(text2, (200, 300))
    #
    for event in pygame.event.get():
        if event.type == QUIT:
            next_wind = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            x_pos = pos[0]
            y_pos = pos[1]
            if 303 + 144 >= x_pos and x_pos >= 303 and y_pos >= 375 and y_pos <= 375 + 144:
                print('ckicked')
                game = True
                width, height = 750, 750
                score = 0
                screen = pygame.display.set_mode((width, height))
                screen.fill('white')
                cleaners = []
                start_fon()
    pygame.display.flip()
    fpsClock.tick(fps)
