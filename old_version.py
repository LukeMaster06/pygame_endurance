"""
WARNING!

If you hate ugly code made by a sophomore in high school during one 48-minute class period, turn away now! Trust me, this isn't pretty.

- Silicontent
"""

# OLD VERSION OF THE GAME

import random
import time
import math
import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 420

POSSIBLE_X = [1, 400, 800]
POSSIBLE_Y = [1, 210, 420]

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# global (hopefully) variables
score = 0
cooldown = 1000


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.speed = 4
        self.size = (20, 20)
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.surf = pygame.Surface(self.size)
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def move(self, pressed):
        if pressed[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


# this code doesn't work. please don't look at it, for my sake.
class PlayerRadius(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerRadius, self).__init__()
        self.rect = pygame.Rect((WIDTH/2, HEIGHT/2), (60, 60))
        self.rect.width = 60
        self.rect.height = 60
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def follow_player(self, player_cent):
        self.rect.center = player_cent


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        if random.randint(0, 1000) == 69:
            self.enemy_size = 200
        else:
            self.enemy_size = random.randint(10, 40)
        self.surf = pygame.Surface((self.enemy_size, self.enemy_size))
        self.surf.fill(RED)
        self.rect = self.surf.get_rect()
        self.speed = 2
        self.rect.x = random.choice(POSSIBLE_X)
        self.rect.y = random.choice(POSSIBLE_Y)
    
    def update(self, player):
        # follow player code courtesy of martineau on Stack Overflow
        # https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def no_spawn(self, collided_with):
        if pygame.sprite.spritecollideany(self, collided_with):
            self.kill()


def update_top(text):
    pygame.display.set_caption(text)


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

KILLENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(KILLENEMY, 5000)

ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 500)

PLAYERBOOST = pygame.USEREVENT + 4

player = Player()
p_rad = PlayerRadius()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
no_go = pygame.sprite.Group()
all_sprites.add(player)
no_go.add(p_rad)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    cooldown -= 1
    if cooldown <= 0:
        cooldown = 0

    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_SPACE and cooldown <= 0:
                player.speed = 10
                pygame.time.set_timer(PLAYERBOOST, 10)
                cooldown = 1000

        if event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == KILLENEMY:
            dead_enemy = random.choice(enemies.sprites())
            enemies.remove(dead_enemy)
            all_sprites.remove(dead_enemy)
            dead_enemy.kill()

        elif event.type == ADDSCORE:
            score += 1
            update_top(f"Score: {score} | Speed Cooldown: {cooldown}")

        elif event.type == PLAYERBOOST:
            player.speed -= 0.05
            if player.speed <= 4:
                player.speed = 4
                pygame.time.set_timer(PLAYERBOOST, 0)

    enemy.no_spawn(no_go)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        update_top(f"Final Score: {score}")
        time.sleep(6)
        running = False

    screen.blit(player.surf, player.rect)
    p_rad.follow_player(player.rect.center)
    player.move(pressed_keys)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    enemies.update(player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
