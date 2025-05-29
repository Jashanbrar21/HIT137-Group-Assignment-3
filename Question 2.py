import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 1 - Player Movement")
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

def main():
    player = Player()
    run = True
    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.update(keys)
        WIN.blit(player.image, player.rect)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
