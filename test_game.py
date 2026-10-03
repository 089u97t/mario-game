import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
GREEN = (0, 180, 0)
WHITE = (255, 255, 255)
x = 100
while True:
    clock.tick(60)
    screen.fill(GREEN)
    text = font.render("Hello from pygbag! Press ENTER", True, WHITE)
    screen.blit(text, (250, 280))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            break
