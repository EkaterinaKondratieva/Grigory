import sys
import pygame
from pygame.locals import *

pygame.init()
fps = 65
fpsClock = pygame.time.Clock()
width, height = 725, 725
screen = pygame.display.set_mode((width, height))


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, sheet2, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cut_sheet2(sheet2, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect.topleft = (x, y)
        self.start_time = pygame.time.get_ticks()
        self.delay = 50

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                    sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = ((pygame.time.get_ticks() - self.start_time) // self.delay) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]


class Slippers(pygame.sprite.Sprite):
    pass


class Cleaner(pygame.sprite.Sprite):
    pass


class Puddle(pygame.sprite.Sprite):
    pass


all_sprites = pygame.sprite.Group()
sheet = pygame.image.load('bear.jpg').convert_alpha()
AnimatedSprite(sheet, 6, 2, 300, 435)
sheet2 = pygame.image.load('slippers.jpg').convert_alpha()
AnimatedSprite(sheet2, 7, 1, 400, 500)

while True:
    screen.fill((255, 255, 255))
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
