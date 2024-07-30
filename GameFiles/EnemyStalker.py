import random
from typing import Callable

import pygame.draw

from .Camera import Camera
from .Enemy import Enemy
from .Helpers import iter_list_reverse
from .Helpers.CommonTypes import Number, Coordinates, IntCoordinates
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class EnemyStalker(Enemy):
    TARGET_RADIUS = 16
    TARGET_RADIUS_SQUARED = TARGET_RADIUS * TARGET_RADIUS
    TARGET_TIME = 10

    TARGET_DISTANCE_PLAYER = 150
    TARGET_DISTANCE_PLAYER_SQUARED = TARGET_DISTANCE_PLAYER * TARGET_DISTANCE_PLAYER

    DAMAGE_TIME: int = 2
    DAMAGE: int = 1

    def __init__(self, x: Number, y: Number, update_offset: int = 0):
        super().__init__(x, y, 32, 32, 100)

        self.target: Coordinates = self.rect.center
        self.target_timer: int = self.TARGET_TIME + update_offset

        self.damage_timer: int = self.DAMAGE_TIME

        self.room_tile_keys: list[IntCoordinates] | None = None
        self._choose_new_tile_as_target: Callable[[Map], None] = self._choose_new_tile_as_target_no_room
        self._target_player: Callable[[Player, Map], bool] = self._target_player_no_room

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

    def _choose_new_tile_as_target_no_room(self, map_: Map) -> None:
        """
        Chooses a tile as a target only if we are not at our target.
        Runs assuming that we are not constrained to a room.
        """

        # If we are not at a target, then do not choose a new tile
        distance_to_target_squared, _, _ = self._distance_to_position_squared(self.target)
        if distance_to_target_squared >= self.TARGET_RADIUS_SQUARED:
            return

        # Get keys for tiles that do not exist that surround the enemy, not including the one we are in
        my_tile_key = map_.tile_key_for_position(self.rect.center)
        surrounding_empty_tile_keys = map_.surrounding_empty_tile_keys(self.rect.centerx, self.rect.centery)
        surrounding_empty_tile_keys.remove(my_tile_key)

        # Get a random choice form those keys
        target_tile_key = random.choice(surrounding_empty_tile_keys)

        # Set our target to the center of the tile
        self.target = (target_tile_key[0] * map_.TILE_SIZE + map_.TILE_SIZE_2,
                       target_tile_key[1] * map_.TILE_SIZE + map_.TILE_SIZE_2)

    def _choose_new_tile_as_target_with_room(self, map_: Map) -> None:
        """
        Chooses a tile as a target only if we are not at our target.
        Runs assuming that we are constrained to a room.
        If there is no valid tile, then go to the center of the tile we are in.
        """

        # If we are not at a target, then do not choose a new tile
        distance_to_target_squared, _, _ = self._distance_to_position_squared(self.target)
        if distance_to_target_squared >= self.TARGET_RADIUS_SQUARED:
            return

        # Get keys for tiles that do not exist that surround the enemy, not including the one we are in
        surrounding_empty_tile_keys = map_.surrounding_empty_tile_keys(self.rect.centerx, self.rect.centery)
        my_tile_key = map_.tile_key_for_position(self.rect.center)
        surrounding_empty_tile_keys.remove(my_tile_key)

        # Remove any keys that are not in the room we are a part of
        room_tile_key: IntCoordinates
        for room_tile_key_index, room_tile_key in iter_list_reverse(surrounding_empty_tile_keys):
            if room_tile_key not in self.room_tile_keys:
                del surrounding_empty_tile_keys[room_tile_key_index]

        # Get a random choice from those keys
        target_tile_key: IntCoordinates
        if surrounding_empty_tile_keys:
            target_tile_key = random.choice(surrounding_empty_tile_keys)
        # If there are no available keys, move to the center of the tile we are in
        else:
            target_tile_key = my_tile_key

        # Set our target to the center of the tile
        self.target = (target_tile_key[0] * map_.TILE_SIZE + map_.TILE_SIZE_2,
                       target_tile_key[1] * map_.TILE_SIZE + map_.TILE_SIZE_2)

    def _target_player_no_room(self, player: Player, map_: Map) -> bool:
        """
        Targets the player if they can be seen.
        Return true if the player has been targeted.
        """

        distance_to_player_squared, *_ = self._distance_to_position_squared(player.rect.center)

        if distance_to_player_squared < self.TARGET_DISTANCE_PLAYER_SQUARED:
            self.target = player.rect.center
            return True
        return False

    def _target_player_with_room(self, player: Player, map_: Map) -> bool:
        """
        Targets the player if they are in the room we are constrained to or if they can be seen.
        Return true if the player has been targeted.
        """

        player_tile_key = map_.tile_key_for_position(player.rect.center)

        if player_tile_key in self.room_tile_keys:
            self.target = player.rect.center
            return True

        distance_to_player_squared, *_ = self._distance_to_position_squared(player.rect.center)
        if distance_to_player_squared < self.TARGET_DISTANCE_PLAYER_SQUARED:
            self.target = player.rect.center
            return True

        return False

    def _update_target(self, player: Player, map_: Map) -> None:
        if self.target_timer > 0:
            self.target_timer -= 1
            return
        self.target_timer = self.TARGET_TIME

        if self._target_player(player, map_):
            return
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
        self.move_x(map_, x_move)

        y_move = y_diff
        if abs(y_diff) > 1:
            y_move = -1 if y_diff < 0 else 1
        self.move_y(map_, y_move)

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        # For now a simple purple circle
        camera_coords = camera.coordinates_to_display_coordinates(self.rect.center)
        pygame.draw.circle(camera.window, (255, 0, 255), camera_coords, 16)

        # Drawing the target
        camera_coords = camera.coordinates_to_display_coordinates(self.target)
        pygame.draw.circle(camera.window, (255, 0, 0), camera_coords, 5)

    def set_room_id(self, room_id: int, map_: Map) -> None:
        """
        Sets the room to be constrained to.
        If the given room id is -1, then clears the set room if it exists.
        """

        if room_id == -1:
            self.room_tile_keys = None
            self._choose_new_tile_as_target = self._choose_new_tile_as_target_no_room
            self._target_player = self._target_player_no_room
        else:
            self.room_tile_keys = map_.rooms[room_id]
            self._choose_new_tile_as_target = self._choose_new_tile_as_target_with_room
            self._target_player = self._target_player_with_room

    def set_center(self, coords: Coordinates):
        self.rect.center = coords
        self.target = coords
