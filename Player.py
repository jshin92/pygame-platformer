import pygame

RED = (255, 0, 0)


class Player:
    def __init__(self, dimensions, screen, tile_map, camera):
        self.screen_width = dimensions[0]
        self.screen_height = dimensions[1]
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

        self.camera = camera

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x - self.camera.x, self.y - self.camera.y,
                                                   self.width, self.height])

    def both_tiles_clear(self, first_tile, second_tile):
        return self.tile_map.tiles[first_tile[0]][first_tile[1]] != 0 and \
               self.tile_map.tiles[second_tile[0]][second_tile[1]] != 0

    # returns the top right and bot right tiles used for collision checking
    def get_right_collisions(self, projected_x):
        return [[int((self.y + 1)/self.tile_map.tile_height),
                 int((projected_x + self.width + 1)/self.tile_map.tile_width)],
                [int((self.y + self.height - 1)/self.tile_map.tile_height),
                 int((projected_x + self.width + 1)/self.tile_map.tile_width)]]

    # returns the bot left and top left tiles used for collision checking
    def get_left_collisions(self, projected_x):
        return [[int((self.y + self.height - 1)/self.tile_map.tile_height),
                 int((projected_x - 1)/self.tile_map.tile_width)],
                [int((self.y + 1)/self.tile_map.tile_height),
                 int((projected_x - 1)/self.tile_map.tile_width)]]

    # returns the top left and top right tiles used for checking if the
    # left side of the player is hitting a tile
    def get_up_collisions(self, projected_y):
        return [[int((projected_y - 1)/self.tile_map.tile_height),
                int((self.x + 1)/self.tile_map.tile_width)],
                [int((projected_y - 1)/self.tile_map.tile_height),
                int((self.x + self.width - 1)/self.tile_map.tile_width)]]

    # returns bot left, bot right
    def get_down_collisions(self, projected_y):
        return [[int((projected_y + self.height + 1)/self.tile_map.tile_height),
                 int((self.x + 1)/self.tile_map.tile_width)],
                [int((projected_y + self.height + 1)/self.tile_map.tile_height),
                 int((self.x + self.width - 1)/self.tile_map.tile_width)]]

    def update(self):
        self.y_velo += self.gravity
        ## check for collision w/ respect to y direction
        # going up (jumping)
        if self.y_velo < 0:
            projected_y = self.y + self.y_velo
            top_left, top_right = self.get_up_collisions(projected_y)
            if self.both_tiles_clear(top_left, top_right):
                self.y = projected_y
            else:
                self.y += (1 + top_left[0]) * self.tile_map.tile_height - self.y
                self.y_velo = 0

        # going down
        else:
            projected_y = self.y + self.y_velo
            bot_left, bot_right = self.get_down_collisions(projected_y)

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
            top_right, bot_right = self.get_right_collisions(projected_x)
            # can move to the right as long as there is no tile blocking the player
            if self.both_tiles_clear(top_right, bot_right) != 0:
                self.x += self.x_velo
            # can't move the projected distance due to a wall, so move as far as possible (delta)
            else:
                self.x += top_right[1] * self.tile_map.tile_width - self.x - self.width
                self.x_velo = 0
        # going left
        elif self.x_velo < 0:
            projected_x = self.x + self.x_velo
            bot_left, top_left = self.get_left_collisions(projected_x)
            if self.both_tiles_clear(bot_left, top_left):
                self.x += self.x_velo
            else:
                self.x += (bot_left[1] + 1) * self.tile_map.tile_width - self.x
                self.x_velo = 0

        # set camera's top left corner such that the player is in the middle
        self.camera.x = min(max(self.x - self.screen_width/2, 0), self.screen_width/2)
        self.camera.y = min(max(self.y - self.screen_height/2, 0), self.screen_height/2)





