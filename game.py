import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 30
size = [400, 400]
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("platformer")

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [0, 0, 40, 40])

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
