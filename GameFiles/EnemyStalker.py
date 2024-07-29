import random

import pygame.draw

from .Camera import Camera
from .Enemy import Enemy
from .Helpers.CommonTypes import Number, Coordinates
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class EnemyStalker(Enemy):
    TARGET_RADIUS = 16
    TARGET_RADIUS_SQUARED = TARGET_RADIUS * TARGET_RADIUS
    TARGET_TIME = 10

    TARGET_DISTANCE_PLAYER = 128
    TARGET_DISTANCE_PLAYER_SQUARED = TARGET_DISTANCE_PLAYER * TARGET_DISTANCE_PLAYER

    DAMAGE_TIME: int = 2
    DAMAGE: int = 1

    def __init__(self, x: Number, y: Number, update_offset: int = 0):
        super().__init__(x, y, 32, 32, 100)

        self.target: Coordinates = self.rect.center
        self.target_timer: int = self.TARGET_TIME + update_offset

        self.damage_timer: int = self.DAMAGE_TIME

    def _distance_to_position_squared(self, position: Coordinates) -> tuple[Number, Number, Number]:
        """
        Calculates the distance to the target.
        Returns the distance squared, the x distance squared, and the y distance squared.
        """

        x_diff = self.rect.centerx - position[0]
        y_diff = self.rect.centery - position[1]
        x_diff_squared = x_diff * x_diff
        y_diff_squared = y_diff * y_diff
        distance_to_target_squared = x_diff_squared + y_diff_squared

        return distance_to_target_squared, x_diff_squared, y_diff_squared

    def _choose_new_tile_as_target(self, map_: Map) -> None:
        """
        Chooses a tile as a target only if we are not at our target.
        """

        # If we are not at a target, then do not choose a new tile
        distance_to_target_squared, _, _ = self._distance_to_position_squared(self.target)
        if distance_to_target_squared >= self.TARGET_RADIUS_SQUARED:
            return

        # Get keys for tiles that do not exist that surround the enemy
        my_tile_key = map_.tile_key_for_position(self.rect.center)
        surrounding_tile_keys_that_exist = map_.surrounding_tile_keys(self.rect.centerx, self.rect.centery)
        surrounding_tile_keys_that_dont_exist = list(
            map_.iter_surrounding_tile_keys(self.rect.centerx, self.rect.centery))
        for tile_key in surrounding_tile_keys_that_exist:
            surrounding_tile_keys_that_dont_exist.remove(tile_key)
        surrounding_tile_keys_that_dont_exist.remove(my_tile_key)

        # Get a random choice for that key
        target_tile_key = random.choice(surrounding_tile_keys_that_dont_exist)

        # Set our target to the center of the tile
        self.target = (target_tile_key[0] * map_.TILE_SIZE + map_.TILE_SIZE_2,
                       target_tile_key[1] * map_.TILE_SIZE + map_.TILE_SIZE_2)

    def _update_target(self, player: Player, map_: Map) -> None:
        if self.target_timer > 0:
            self.target_timer -= 1
            return
        self.target_timer = self.TARGET_TIME

        _temp = self._distance_to_position_squared(player.rect.center)
        distance_to_player_squared, x_diff_squared, y_diff_squared = _temp

        # If we can see the player, target the player
        if distance_to_player_squared < self.TARGET_DISTANCE_PLAYER_SQUARED:
            self.target = player.rect.center
        # If we cannot see the player, chose a random tile to move to
        else:
            self._choose_new_tile_as_target(map_)

    def _damage_player(self, player: Player) -> None:
        if self.rect.colliderect(player.rect):
            if self.damage_timer >= 0:
                self.damage_timer -= 1
                return

            self.damage_timer = self.DAMAGE_TIME
            player.deal_damage(self.DAMAGE)

    def update(self, player: Player, map_: Map, potion_handler: PotionHandler) -> None:
        self._update_target(player, map_)
        self._damage_player(player)

    def move(self, map_: Map) -> None:
        x_diff = self.target[0] - self.rect.centerx
        y_diff = self.target[1] - self.rect.centery

        x_diff_squared = x_diff * x_diff
        y_diff_squared = y_diff * y_diff

        distance_squared = x_diff_squared + y_diff_squared

        # If at target then do not move
        if distance_squared < self.TARGET_RADIUS_SQUARED:
            return

        x_move = x_diff
        if abs(x_diff) > 1:
            x_move = -1 if x_diff < 0 else 1

        y_move = y_diff
        if abs(y_diff) > 1:
            y_move = -1 if y_diff < 0 else 1

        # Move to target
        self.move_x(map_, x_move)
        self.move_y(map_, y_move)

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        # For now a simple purple circle
        camera_coords = camera.coordinates_to_display_coordinates(self.rect.center)
        pygame.draw.circle(camera.window, (255, 0, 255), camera_coords, 16)

        # Drawing the target
        # camera_coords = camera.coordinates_to_display_coordinates(self.target)
        # pygame.draw.circle(camera.window, (255, 0, 0), camera_coords, 5)
