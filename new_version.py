# NEW VERSION WITH DASH KILLING
import random
import math
import time
import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 420

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
ORANGE = (255, 130, 0)

SPAWNPOINTS = [
    (1, 1),
    (WIDTH/2, 1),
    (WIDTH, 1),
    (1, HEIGHT/2),
    (1, HEIGHT),
    (HEIGHT, 1),
    (HEIGHT, WIDTH/2),
    (HEIGHT, WIDTH),
    (WIDTH, HEIGHT/2),
    (WIDTH, HEIGHT)
]

score = 0
killed = 0
cooldown = 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()
pygame.display.set_caption("Endurance")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.size = (20, 20)
        self.speed = 4
        self.invincible = False
        self.surf = pygame.Surface(self.size)
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT/2))

    def move(self, pressed):
        if pressed[K_UP] or pressed[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed[K_DOWN] or pressed[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed[K_LEFT] or pressed[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed[K_RIGHT] or pressed[K_d]:
            self.rect.move_ip(self.speed, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.speed = 2

        if random.randint(0, 1000) == 69:
            self.enemy_size = 200
        else:
            self.enemy_size = random.randint(10, 40)
        
        if random.randint(0, 20) == 10:
            self.color = PURPLE
            self.speed = 4
        elif random.randint(0, 40) == 10:
            self.color = ORANGE
            self.speed = 0.5
            self.enemy_size = 70
        else:
            self.color = RED
            self.speed = 2
        
        self.surf = pygame.Surface((self.enemy_size, self.enemy_size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
        self.rect.center = random.choice(SPAWNPOINTS)
    
    def update(self, player):
        # follow player code courtesy of martineau on Stack Overflow
        # https://stackoverflow.com/questions/20044791/how-to-make-an-enemy-follow-the-player-in-pygame
        try:
            dx, dy = player.rect.x - self.rect.x, player.rect.y -   self.rect.y
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        except ZeroDivisionError:
            print("/0 is no")


# end of class creation
# font rendering
font = pygame.font.SysFont("monospace", 15)


def load_hud():
    hud = font.render(f"{score} | Killed: {killed} | Cooldown: {cooldown}", 1, (BLACK))
    hud_2 = font.render(f"Invincible: {player.invincible}", 1, (BLACK))
    screen.blit(hud, (10, 10))
    screen.blit(hud_2, (10, 30))


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

KILLENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(KILLENEMY, 5000)

ADDSCORE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDSCORE, 500)

PLAYERBOOST = pygame.USEREVENT + 4

player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites.add(player)

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
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE and cooldown <= 0:
                player.invincible = True
                player.speed = 10
                pygame.time.set_timer(PLAYERBOOST, 10)
                cooldown = 500
        
        elif event.type == QUIT:
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

        elif event.type == PLAYERBOOST:
            player.speed -= 0.05
            if player.speed <= 4:
                player.speed = 4
                player.invincible = False
                pygame.time.set_timer(PLAYERBOOST, 0)

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for collided_with in hits:
        if player.invincible == True:
            killed += 1
            score += 2
        else:
            player.kill()
            time.sleep(6)
            running = False

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    player.move(pressed_keys)
    player.rect.clamp_ip(screen_rect)

    enemies.update(player)

    load_hud()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
