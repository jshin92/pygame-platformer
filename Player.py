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
        self.friction = .90

        self.x_accel = 0

        self.moving_left = False
        self.moving_right = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.width, self.height])

    def both_tiles_clear(self, first_tile, second_tile):
        return self.tile_map.tiles[first_tile[0]][first_tile[1]] != 0 and \
               self.tile_map.tiles[second_tile[0]][second_tile[1]] != 0

    # returns corners in order of:
    # top_left, top_right, bot_left, bot_right
    def calculate_corners(self, dir, projected_x, projected_y):
        if dir == "UPDOWN":
            projected_dir = projected_y
        elif dir == "LEFTRIGHT":
            projected_dir = projected_x

        top_left = [int(projected_dir / self.tile_map.tile_height),
                    int(self.x / self.tile_map.tile_width)]

        top_right = [int(projected_dir / self.tile_map.tile_height),
                     int((self.x + self.width) / self.tile_map.tile_width)]

        bot_left = [int((projected_dir + self.height) / self.tile_map.tile_height),
                    int(self.x / self.tile_map.tile_width)]

        bot_right = [int((projected_dir + self.height) / self.tile_map.tile_height),
                     int((self.x + self.width) / self.tile_map.tile_width)]

        return top_left, top_right, bot_left, bot_right

    # returns [row, col] of block to right of player
    def get_block_to_right(self, projected_x):
        return [int((self.y + self.height - 1)/self.tile_map.tile_height),
                int((projected_x + self.width + 1)/self.tile_map.tile_width)]

    # returns [row, col] of block bottom left of player
    def get_bot_left(self, projected_x):
        return [int((self.y + self.height - 1)/self.tile_map.tile_height),
                int((projected_x - 1)/self.tile_map.tile_width)]

    # returns [row, col] of block top left of player
    def get_top_left(self, projected_x):
        return [int((self.y + 1)/self.tile_map.tile_height),
                int((projected_x - 1)/self.tile_map.tile_width)]

    def update(self):
        self.y_velo += self.gravity
        ## check for collision w/ respect to y direction
        # going up (jumping)
        # TODO: DO GOING UP LOGIC!
        if self.y_velo < 0:
            pass
        # going down
        else:
            projected_y = self.y + self.y_velo
            _, _, bot_left, bot_right = self.calculate_corners("UPDOWN", 0, projected_y)

            # only fall down if both tiles below player are blank
            if self.both_tiles_clear(bot_left, bot_right):
                self.y = projected_y
            else:
                # can't translate full projected length--block in way, so
                # go the delta
                self.y += self.tile_map.tile_height * bot_left[0] - self.y - self.height
                self.y_velo = 0

        ## check for collision w/ respect to x direction
        self.x_velo += self.x_accel
        self.x_velo *= self.friction
        # going right
        if self.x_velo > 0:
            projected_x = self.x + self.x_velo
            right_block = self.get_block_to_right(projected_x)
            # can move to the right as long as there is no tile blocking the player
            if self.tile_map.tiles[right_block[0]][right_block[1]] != 0:
                self.x += self.x_velo
            # can't move the projected distance due to a wall, so move as far as possible (delta)
            else:
                self.x += right_block[1] * self.tile_map.tile_width - self.x - self.width
                self.x_velo = 0
        # going left
        elif self.x_velo < 0:
            projected_x = self.x + self.x_velo
            bot_left = self.get_bot_left(projected_x)
            top_left = self.get_top_left(projected_x)
            if self.tile_map.tiles[bot_left[0]][bot_left[1]] != 0 and self.tile_map.tiles[top_left[0]][top_left[1]] != 0:
                self.x += self.x_velo
            else:
                self.x += (bot_left[1] + 1) * self.tile_map.tile_width - self.x
                self.x_velo = 0





