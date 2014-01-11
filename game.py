import pygame
import Tile_Map
import Player
import Camera

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

FPS = 30
dimensions = [400, 400]
pygame.init()
screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Platformer")

tile_map = Tile_Map.TileMap()
camera = Camera.Camera()
player = Player.Player(dimensions, screen, tile_map, camera)

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_accel -= 3
            elif event.key == pygame.K_RIGHT:
                player.x_accel += 3
            elif event.key == pygame.K_SPACE:
                player.y_velo = -12
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.x_accel = 0
            elif event.key == pygame.K_RIGHT:
                player.x_accel = 0


    player.update()
    screen.fill(BLACK)
    for row in range(tile_map.num_rows):
        for col in range(tile_map.num_cols):
            cur_tile = tile_map.tiles[row][col]
            if cur_tile == 0:
                cur_color = BLACK
            elif cur_tile == 1:
                cur_color = WHITE
            elif cur_tile == 2:
                cur_color = BLUE
            pygame.draw.rect(screen, cur_color, [tile_map.tile_width * col - camera.x,
                                                 tile_map.tile_height * row - camera.y,
                                                 tile_map.tile_width,
                                                 tile_map.tile_height])
    player.draw()

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
