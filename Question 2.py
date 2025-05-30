import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Game - Day 4")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
FONT = pygame.font.SysFont(None, 24)

# ---------------- Classes ----------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(50, HEIGHT - 100))
        self.health = 100
        self.lives = 3
        self.jump_power = -20
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True
        self.damage_timer = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]: self.rect.x -= 5
        if keys[pygame.K_RIGHT]: self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.rect.y >= HEIGHT - 100:
            self.rect.y = HEIGHT - 100
            self.velocity_y = 0
            self.on_ground = True
        if self.damage_timer > 0:
            self.damage_timer -= 1


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.damage = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=350):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health
        self.passed = False

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 200))
        self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect(midbottom=(WIDTH + 100, HEIGHT - 40))
        self.health = 4000
        self.passed = False

    def update(self):
        self.rect.x -= 1
        if self.rect.right < 0:
            self.kill()


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.type = type
        if type == 'health':
            self.image.fill((0, 255, 0))
        elif type == 'life':
            self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x -= 2
        if self.rect.right < 0:
            self.kill()

# ---------------- Utility Functions ----------------

def draw_text(text, size, color, y_offset):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    WIN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + y_offset))

def draw_health_bar(x, y, value, max_value, width=100):
    pygame.draw.rect(WIN, (255, 0, 0), (x, y, width, 10))
    pygame.draw.rect(WIN, (0, 255, 0), (x, y, max(0, width * (value / max_value)), 10))

def game_over_screen(score):
    WIN.fill(WHITE)
    draw_text("GAME OVER", 48, (0, 0, 0), -40)
    draw_text(f"Score: {score}", 32, (0, 0, 0), 10)
    draw_text("Press R to Restart or ESC to Exit", 24, (0, 0, 0), 50)
    pygame.display.update()
    wait_for_restart()

def win_screen(score):
    WIN.fill(WHITE)
    draw_text("YOU WIN!", 48, (0, 128, 0), -40)
    draw_text(f"Final Score: {score}", 32, (0, 0, 0), 10)
    draw_text("Press R to Restart or ESC to Exit", 24, (0, 0, 0), 50)
    pygame.display.update()
    wait_for_restart()

def wait_for_restart():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

# ---------------- Main Game Function ----------------

def main():
    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    score = 0
    level = 1
    boss_spawned = False
    spawn_timer = 0
    collect_timer = 0

    run = True
    while run:
        clock.tick(60)
        WIN.fill(WHITE)
        spawn_timer += 1
        collect_timer += 1

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.update(keys)

        if keys[pygame.K_f]:
            bullets.add(Projectile(player.rect.right, player.rect.centery))

        # Enemy spawn before boss
        if spawn_timer % 200 == 0 and level < 3:
            enemies.add(Enemy(WIDTH, HEIGHT - 100))

        # Collectible spawns
        if collect_timer % 400 == 0:
            collectibles.add(Collectible(WIDTH, HEIGHT - 120, 'health'))
        if collect_timer % 600 == 0:
            collectibles.add(Collectible(WIDTH, HEIGHT - 120, 'life'))

        # Level update
        if score < 30:
            level = 1
        elif score < 60:
            level = 2
        else:
            level = 3

        # Spawn boss once
        if level == 3 and not boss_spawned:
            enemies.add(BossEnemy())
            boss_spawned = True

        # Bullet hits
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                enemy.health -= bullet.damage
                bullet.kill()
                if enemy.health <= 0:
                    enemy.kill()
                    score += 100 if isinstance(enemy, BossEnemy) else 5
                    if isinstance(enemy, BossEnemy):
                        win_screen(score)
                        return

        # Collectibles
        for c in pygame.sprite.spritecollide(player, collectibles, True):
            if c.type == 'health':
                player.health = min(100, player.health + 20)
            elif c.type == 'life':
                player.lives += 1

        # Avoidance score
        for enemy in enemies:
            if not enemy.passed and enemy.rect.right < player.rect.left:
                enemy.passed = True
                score += 2

        # Enemy collision
        if pygame.sprite.spritecollide(player, enemies, False):
            if player.damage_timer == 0:
                player.health -= 10
                player.damage_timer = 60
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100
                    if player.lives <= 0:
                        game_over_screen(score)
                        return

        bullets.update()
        enemies.update()
        collectibles.update()

        WIN.blit(player.image, player.rect)
        bullets.draw(WIN)
        enemies.draw(WIN)
        collectibles.draw(WIN)

        # Draw health bars
        for enemy in enemies:
            max_hp = 4000 if isinstance(enemy, BossEnemy) else 350
            bar_width = 80 if isinstance(enemy, BossEnemy) else 40
            draw_health_bar(enemy.rect.x, enemy.rect.y - 10, enemy.health, max_hp, bar_width)

        draw_health_bar(10, 10, player.health, 100)
        WIN.blit(FONT.render(f"Lives: {player.lives}", True, (0, 0, 0)), (10, 25))
        WIN.blit(FONT.render(f"Score: {score}", True, (0, 0, 0)), (10, 40))
        WIN.blit(FONT.render(f"Level: {level}", True, (0, 0, 0)), (10, 55))

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
