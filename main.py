#! /usr/bin/env python

import os
import random
import time

import pygame
from pygame import gfxdraw

# based on https://pythonprogramming.altervista.org/simple-labytinth-in-pygame/

class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy, walls):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
        self.collision(dx, dy, walls)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def collision(self, dx, dy, walls):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom


class Wall(object):

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


class Level:
    def __init__(self, levelString:str):
        self.level = levelString.splitlines()[1:]

    def __iter__(self):
        for line in self.level:
            yield line

class Game:
    def __init__(self, player:Player, level:Level):
        self.player = player
        self.walls = []
        self.end_rect = None # yet; determined when loading level
        self.load_level(level)

    def load_level(self, level:Level):
        # Parse the level string. W = wall, E = exit
        x = y = 1
        self.walls = []
        for row in level:
            for col in row:
                if col == "W":
                    wall = Wall((x, y))
                    self.walls.append(wall)
                if col == "E":
                    self.end_rect = pygame.Rect(x, y, 10, 10)
                x += 18
            y += 18
            x = 1
        pass

    def run(self):
        pygame.init()

        pygame.display.set_caption("Get to the red square!")
        screen = pygame.display.set_mode((360, 270))

        clock = pygame.time.Clock()
        running = True
        back = pygame.image.load("back.png")
        pygame.event.clear()
        start = None
        startPos = self.player.rect.center
        while running:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

            # Move the player if an arrow key is pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                player.move(-2, 0, self.walls)
            if key[pygame.K_RIGHT]:
                player.move(2, 0, self.walls)
            if key[pygame.K_UP]:
                player.move(0, -2, self.walls)
            if key[pygame.K_DOWN]:
                player.move(0, 2, self.walls)
            if start is None and player.rect.center != startPos:
                start = time.time()

            # Just added this to make it slightly fun ;)
            if player.rect.colliderect(self.end_rect):
                return time.time() - start

            # Draw the scene
            screen.blit(back, (0, 0))
            for wall in game.walls:
                pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
            pygame.draw.rect(screen, (255, 0, 0), self.end_rect)
            pygame.draw.rect(screen, (255, 200, 0), player.rect)
            # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
            pygame.display.flip()
            clock.tick(120)


os.environ["SDL_VIDEO_CENTERED"] = "1"
player = Player()
level = Level("""
WWWWWWWWWWWWWWWWWWWW
W                  W
W         WWWWWW   W
W   WWWW       W   W
W   W        WWWW  W
W WWW  WWWW        W
W   W     W W      W
W   W     W   WWW WW
W   WWW WWW   W W  W
W     W   W   W W  W
WWW   W   WWWWW W  W
W W      WW        W
W W   WWWW   WWW   W
W     W    E   W   W
WWWWWWWWWWWWWWWWWWWW
""")
game = Game(player, level)
game.load_level(level)
secs = game.run()
print(f'you played {secs:.2f} seconds')
pygame.quit()

# other level:
level2 = Level("""
WWWWWWWWWWWWWWWWWWWW
W                  W
W  S               W
WWWWWWWW WWWWWWWWWWW
W            W  W  W
WWW WWWWWWWWWW     W
W               W  W
WWWWWWWWWWWWWW  W  W    
W             WWW  W
WW WWWWWWWWWW      W
W           WWWWWWWW 
WWW WWWWWWWWW   E  W
W   W   W   W      W
W     W   W   W    W
WWWWWWWWWWWWWWWWWWWW
""")
