import pygame

RED = (255, 0, 0)


class Player:
    def __init__(self, screen, tile_map):
        self.screen = screen
        self.tile_map = tile_map
        self.color = RED
        self.x = 70
        self.y = 40
        self.width = 20
        self.height = 20

        self.x_velo = 0
        self.y_velo = 0
        self.gravity = .5
        self.friction = .9

        self.x_accel = 0
        self.y_accel = 0

        self.moving_left = False
        self.moving_right = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.width, self.height])

    def update(self):
        self.y_velo += self.gravity
        ## check for collision w/ respect to y direction
        cur_tile_row = int(self.y // self.tile_map.tile_height)
        closest_blocked_tile_row = -1
        # going up (jumping)
        # TODO: DO GOING UP LOGIC!
        if self.y_velo < 0:
            pass
        # going down
        else:
            left_line_col = int(self.x // self.tile_map.tile_width)
            right_line_col = int((self.x + self.width) // self.tile_map.tile_width)

            # find closest tile that blocks the player
            for row in range(cur_tile_row, self.tile_map.num_rows):
                for col in range(left_line_col, right_line_col + 1):
                    if self.tile_map.tiles[row][col] == 0:
                        closest_blocked_tile_row = row
                        break
                if closest_blocked_tile_row != -1:
                    break

            block_dist = closest_blocked_tile_row * self.tile_map.tile_height - self.y - self.height
            # can move only by the minimum betwixt the distance from the player to the nearest thing
            # blocking it or the distance that it wanted to go
            self.y += min(self.y_velo, block_dist)
            # can't move down when on top of a block
            if block_dist == 0:
                self.y_velo = 0

        ## check for collision with respect to the x direction
        self.x_velo += self.x_accel
        self.x_velo *= self.friction
        self.x += self.x_velo


