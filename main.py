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
    def __init__(self, x, y, group):
        super().__init__(all_sprites)
        self.image = pygame.sprite.Sprite()
        self.image = pygame.image.load('cleaner.jpeg')
        self.image = pygame.transform.scale(self.image, (160, 160))
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x - 75, self.y + 75)
        self.mask = pygame.mask.from_surface(self.image)
        self.time = pygame.time.get_ticks()
        self.start = random.choice([0, 2, 1, 3]) * 1000
        self.add(group)

    def update(self, *args):
        if self.rect.x <= 750 + 160:
            self.rect.x += 3
        else:
            self.rect.x = -160


class Puddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.sprite.Sprite()
        self.image = pygame.image.load('puddle.png')
        self.image.set_colorkey('white')
        self.image = pygame.transform.scale(self.image, (750, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        self.add(puddles)


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


def cleaners_in_line(x, y, type):
    if type == 1:
        Cleaner(x - 160, y, cleaners)
        Cleaner(x - 500, y, cleaners)
        Cleaner(x - 830, y, cleaners)
    elif type == 2:
        Cleaner(x - 200, y, cleaners)
        Cleaner(x - 520, y, cleaners)
        Cleaner(x - 890, y, cleaners)
    else:
        Cleaner(x - 350, y, cleaners)
        Cleaner(x, y, cleaners)
        Cleaner(x - 500, y, cleaners)


def start_fon():
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    pygame.mixer.music.set_volume(0.2)
    for i in range(3):
        num = random.choice([1, 2, 3])
        # 1 cleaner
        # 2 puddle
        # 3 slipers
        if num == 3:
            Carpet(0, 150 * i)
            # Slipers(0, 150 * i)
        elif num == 1:
            Floor(0, 150 * i)
            (Cleaner(0, 150 * i, cleaners))
            type = random.choice([1, 2, 3])
            cleaners_in_line(0, 150 * i, type)
        else:
            Floor(0, 150 * i)
            (Puddle(0, 145 * i))
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


def hello_screen():
    screen.fill('white')
    font = pygame.font.SysFont('comicsansms', 35)

    text = font.render('Правила игры:', True, (0, 0, 0))
    screen.blit(text, (250, 300))

    text2 = font.render('1) Под пылесосы попадать нельзя', True, (0, 0, 0))
    screen.blit(text2, (90, 350))

    text3 = font.render('2) На лужах нельзя долго стоять', True, (0, 0, 0))
    screen.blit(text3, (100, 400))

    text4 = font.render('3) Если попадаешь под спрей - умираешь', True, (0, 0, 0))
    screen.blit(text4, (25, 450))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        fpsClock.tick(fps)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

fail_sound = pygame.mixer.Sound('fail.wav')
fps = 60
fpsClock = pygame.time.Clock()
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
all_sprites = pygame.sprite.Group()

cleaners = pygame.sprite.Group()
puddles = pygame.sprite.Group()

hello_screen()

start_fon()

cockroach = Cockroach()

camera = Camera()

pygame.font.init()
font = pygame.font.SysFont('comicsansms', 35)

score = 0

all_results = []
game = True
next_wind = True
have_collision_with_puddle = False
while next_wind:
    while game:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                cockroach.move()
                for puddle in puddles:
                    if pygame.sprite.collide_mask(puddle, cockroach):
                        time = pygame.time.get_ticks()
                        have_collision_with_puddle = True
                        break
                else:
                    have_collision_with_puddle = False

                score += 1
                num = random.choice([1, 2, 3, 4])
                # 1 cleaner
                # 2 puddle
                # 3 slipers
                # 4 floor
                if num == 1:
                    Floor(0, -150)
                    (Cleaner(50, -150, cleaners))
                    type = random.choice([1, 2, 3])
                    cleaners_in_line(750, -150, type)
                elif num == 2:
                    Floor(0, -150)
                    (Puddle(0, -150))
                elif num == 3:
                    Carpet(0, -150)
                    # Slipers(0, -150)
                elif num == 4:
                    Floor(0, -150)

        # Update
        cleaners.update()

        camera.update(cockroach)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        if cockroach.colllision():
            game = False
            fail_sound.play(0)
            all_results.append(score)

        if have_collision_with_puddle:
            if pygame.time.get_ticks() - time >= 3000:
                game = False
                fail_sound.play(0)
                all_results.append(score)

        # Draw
        all_sprites.draw(screen)
        screen.blit(cockroach.get_image(), (cockroach.x, cockroach.y))
        text = font.render(str(score), True, (0, 0, 0))
        screen.blit(text, (375, 0))
        pygame.display.flip()
        fpsClock.tick(fps)

    #######
    pygame.mixer.music.stop()

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
                game = True
                width, height = 750, 750
                score = 0
                screen = pygame.display.set_mode((width, height))
                screen.fill('white')
                cleaners = pygame.sprite.Group()
                puddles = pygame.sprite.Group()
                have_collision_with_puddle = False
                start_fon()
                fail_sound.stop()
                pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)

    pygame.display.flip()
    fpsClock.tick(fps)
