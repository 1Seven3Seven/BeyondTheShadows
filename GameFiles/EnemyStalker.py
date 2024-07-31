import pygame
import random
from typing import Callable

from .Camera import Camera
from .Enemy import Enemy
from .Helpers import iter_list_reverse
from .Helpers.CommonTypes import Number, Coordinates, IntCoordinates
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class _Circle:
    INITIAL_RADIUS = 30
    RADIUS_DECAY = INITIAL_RADIUS / 100

    def __init__(self, x: Number, y: Number, vx: Number, vy: Number):
        self.x: Number = x
        self.y: Number = y

        self.vx: Number = vx
        self.vy: Number = vy

        self.radius: Number = self.INITIAL_RADIUS

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy

        self.radius -= self.RADIUS_DECAY

    def __str__(self) -> str:
        return f"Circle({round(self.x, 3)}, {round(self.y, 3)}, {round(self.radius, 3)})"

    def __repr__(self) -> str:
        return self.__str__()


class EnemyStalker(Enemy):
    TARGET_RADIUS = 16
    TARGET_RADIUS_SQUARED = TARGET_RADIUS * TARGET_RADIUS
    TARGET_TIME = 10

    TARGET_DISTANCE_PLAYER = 150
    TARGET_DISTANCE_PLAYER_SQUARED = TARGET_DISTANCE_PLAYER * TARGET_DISTANCE_PLAYER

    DAMAGE_TIME: int = 2
    DAMAGE: int = 1

    CIRCLE_TIMER: int = 3

    def __init__(self, x: Number, y: Number, update_offset: int = 0):
        super().__init__(x, y, 32, 32, 100)

        self.target: Coordinates = self.rect.center
        self.target_timer: int = self.TARGET_TIME + update_offset

        self.damage_timer: int = self.DAMAGE_TIME

        self.room_tile_keys: list[IntCoordinates] | None = None
        self._choose_new_tile_as_target: Callable[[Map], None] = self._choose_new_tile_as_target_no_room
        self._target_player: Callable[[Player, Map], bool] = self._target_player_no_room

        self.circles: list[_Circle] = []
        self.circle_timer: int = self.CIRCLE_TIMER

        self.sprite: pygame.Surface = pygame.Surface((self.rect.w + _Circle.INITIAL_RADIUS * 4,
                                                      self.rect.h + _Circle.INITIAL_RADIUS * 4))
        self.sprite_rect = self.sprite.get_rect()

        self.sub_sprite: pygame.Surface = pygame.Surface((_Circle.INITIAL_RADIUS * 2, _Circle.INITIAL_RADIUS * 2))
        self.sub_sprite_rect = self.sub_sprite.get_rect()

        self.updating: bool = False

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
        if self.updating:
            self._update_target(player, map_)
            self._damage_player(player)
        else:
            player_tile_key = map_.tile_key_for_position(player.rect.center)
            if player_tile_key in self.room_tile_keys:
                self.updating = True

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

    def _update_circles_for_sprite(self) -> None:
        # Update the circles
        circle: _Circle
        for circle_index, circle in iter_list_reverse(self.circles):
            if circle.radius <= 0:
                del self.circles[circle_index]
                continue

            circle.update()

        # Add new circles
        if self.circle_timer > 0:
            self.circle_timer -= 1
            return

        self.circle_timer = self.CIRCLE_TIMER

        self.circles.append(
            _Circle(
                self.sprite.get_width() // 2, self.sprite.get_height() // 2,
                random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)
            )
        )

    def _render_sprite(self) -> None:
        self.sprite.fill((0, 0, 0))  # NOQA: Duplicate code from basic enemy

        for circle in self.circles:
            self.sub_sprite.fill((0, 0, 0))
            pygame.draw.circle(self.sub_sprite, (10, 10, 10),
                               (self.sub_sprite.get_width() // 2, self.sub_sprite.get_height() // 2),
                               circle.radius)

            self.sub_sprite_rect.center = circle.x, circle.y
            self.sprite.blit(self.sub_sprite, self.sub_sprite_rect, special_flags=pygame.BLEND_RGB_ADD)

    def draw(self, camera: Camera) -> None:
        self.sprite_rect.center = self.rect.center

        if not camera.can_see(self.sprite_rect):
            return

        self._update_circles_for_sprite()
        self._render_sprite()
        camera.convert_rect_to_camera_coordinates(self.sprite_rect)
        camera.window.blit(self.sprite, self.sprite_rect, special_flags=pygame.BLEND_RGB_SUB)

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
