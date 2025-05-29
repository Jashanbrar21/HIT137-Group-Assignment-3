# Builds on Day 1 by adding projectiles and basic enemies

import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 2 - Shooting & Enemies")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(50, HEIGHT - 100))
        self.velocity_y = 0
        self.jump_power = -20
        self.gravity = 1
        self.on_ground = True

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.y >= HEIGHT - 100:
            self.rect.y = HEIGHT - 100
            self.velocity_y = 0
            self.on_ground = True

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

def main():
    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    spawn_timer = 0
    run = True
    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        keys = pygame.key.get_pressed()
        spawn_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.update(keys)

        if keys[pygame.K_f]:
            bullets.add(Projectile(player.rect.right, player.rect.centery))

        if spawn_timer % 100 == 0:
            enemies.add(Enemy(WIDTH, HEIGHT - 100))

        bullets.update()
        enemies.update()

        WIN.blit(player.image, player.rect)
        bullets.draw(WIN)
        enemies.draw(WIN)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
