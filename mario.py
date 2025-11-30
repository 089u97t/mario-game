import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
GAME_TOP_MARGIN = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Adventure")

# colors
GREEN_BG = (0, 180, 0)
RED_BRICK = (150, 40, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)
BLUE = (0, 120, 255)

# Fonts
font = pygame.font.SysFont("comicsansms", 28)
title_font = pygame.font.SysFont("comicsansms", 60)

# Game constants
PLAYER_WIDTH, PLAYER_HEIGHT = 45, 60
PLAYER_SPEED = 5
PLAYER_JUMP = 16
GRAVITY = 0.6
FPS = 60

WORLD_WIDTH = 2000  # total world width (larger than screen)

# ======= Classes =====
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # <-- fixed: this was the place the original typo likely occurred
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - PLAYER_HEIGHT - 100
        self.vel_y = 0
        self.on_ground = False
        self.draw_robot()

    def draw_robot(self):
        """ Draw robot-like player """
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, GRAY, (5, 10, 35, 45))  # body
        pygame.draw.rect(self.image, DARK_GRAY, (10, 5, 25, 10))  # hat base
        pygame.draw.rect(self.image, BLUE, (5, 0, 35, 5))  # hat top
        pygame.draw.circle(self.image, WHITE, (17, 30), 4)  # left eye
        pygame.draw.circle(self.image, WHITE, (30, 30), 4)  # right eye
        pygame.draw.rect(self.image, BLACK, (17, 34, 4, 2))
        pygame.draw.rect(self.image, BLACK, (30, 34, 4, 2))

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Gravity
        self.vel_y += GRAVITY
        self.rect.y += int(self.vel_y)

        # Platform collision (simple, only handles landing from above)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and self.vel_y >= 0:
                # check if player was falling and intersects top of platform
                if self.rect.bottom - self.vel_y <= p.rect.top + 5:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True

        # Jump (space)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -PLAYER_JUMP

        # Keep inside world bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WORLD_WIDTH - PLAYER_WIDTH:
            self.rect.x = WORLD_WIDTH - PLAYER_WIDTH
        # prevent falling below ground (safety)
        if self.rect.y > HEIGHT:
            self.rect.y = HEIGHT - PLAYER_HEIGHT
            self.vel_y = 0
            self.on_ground = True

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        # Use non-alpha surface for brick look
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.draw_bricks()

    def draw_bricks(self):
        """Draw brick pattern"""
        self.image.fill(RED_BRICK)
        pygame.draw.rect(self.image, WHITE, (0, 0, self.rect.width, self.rect.height), 2)
        # Add horizontal lines for bricks
        for yy in range(5, self.rect.height, 10):
            pygame.draw.line(self.image, WHITE, (0, yy), (self.rect.width, yy), 1)
        for xx in range(10, self.rect.width, 20):
            pygame.draw.line(self.image, WHITE, (xx, 0), (xx, self.rect.height), 1)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 9)
        pygame.draw.circle(self.image, (255, 255, 120), (10, 10), 5)
        self.rect = self.image.get_rect(center=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((45, 35), pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.choice((-3, 3))
        # bounds relative to starting center x
        self.left_bound = x - 100
        self.right_bound = x + 100

    def update(self):
        self.rect.x += self.speed
        # reverse if out of bounds
        if self.rect.x < self.left_bound or self.rect.x > self.right_bound:
            self.speed *= -1

# ===== Screens =====
def start_screen():
    while True:
        screen.fill(GREEN_BG)
        title = title_font.render("Mario Adventure", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def game_over_screen(score):
    while True:
        screen.fill(GREEN_BG)
        over_text = title_font.render("Game Over!", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ==== Main Game ==== 
def main_game():
    level = 1
    score = 0
    player = Player()

    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Ground
    ground = Platform(0, HEIGHT - 40, WORLD_WIDTH, 40)
    platforms.add(ground)

    # Random platforms and coins spread across world
    for _ in range(20):
        x = random.randint(100, WORLD_WIDTH - 150)
        y = random.randint(GAME_TOP_MARGIN + 100, HEIGHT - 150)
        p = Platform(x, y, 120, 15)
        platforms.add(p)
        for _ in range(random.randint(1, 3)):
            cx = x + random.randint(10, 100)
            cy = y - random.randint(40, 100)
            # ensure coin vertically makes sense (not below platform)
            if cy < 0:
                cy = 10
            c = Coin(cx, cy)
            coins.add(c)

    for _ in range(10):
        ex = random.randint(200, WORLD_WIDTH - 200)
        ey = random.randint(GAME_TOP_MARGIN + 200, HEIGHT - 80)
        e = Enemy(ex, ey)
        enemies.add(e)

    clock = pygame.time.Clock()
    camera_x = 0  # Camera offset
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(GREEN_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Updates
        player.update(platforms)
        enemies.update()

        # Scroll camera when player moves near edges
        if player.rect.x - camera_x > WIDTH * 0.6:
            camera_x += PLAYER_SPEED
        if player.rect.x - camera_x < WIDTH * 0.3 and camera_x > 0:
            camera_x -= PLAYER_SPEED

        # Clamp camera to world edges
        camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))

        # Coin collection
        hit_coins = pygame.sprite.spritecollide(player, coins, True)
        score += len(hit_coins) * 10

        # Enemy collision -> game over
        if pygame.sprite.spritecollide(player, enemies, False):
            choice = game_over_screen(score)
            if choice == "restart":
                return "restart"  # caller can restart the whole game loop
            else:
                return  # end

        # Draw top HUD
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, GAME_TOP_MARGIN))
        score_text = font.render(f"Score: {score}", True, BLACK)
        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (20, 10))
        screen.blit(level_text, (WIDTH - 150, 10))

        # Draw game world with camera offset
        for group in (platforms.sprites(), coins.sprites(), enemies.sprites(), [player]):
            for obj in group:
                screen.blit(obj.image, (obj.rect.x - camera_x, obj.rect.y))

        pygame.display.flip()

# Run the game with restart loop
while True:
    start_screen()
    result = main_game()
    if result != "restart":
        break

pygame.quit()
