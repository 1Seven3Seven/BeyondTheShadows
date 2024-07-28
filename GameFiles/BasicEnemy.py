import random
from dataclasses import dataclass

import pygame

from .Camera import Camera
from .Enemy import Enemy
from .Map import Map
from .Player import Player

CIRCLE_SPAWN_DELAY = 3
CIRCLE_RADIUS = 30
CIRCLE_RADIUS_10 = CIRCLE_RADIUS / 100.0

TARGET_RADIUS = 16
TARGET_RADIUS_SQUARED = TARGET_RADIUS * TARGET_RADIUS
TARGET_DELAY = 60


@dataclass
class Circle:
    x: int | float
    y: int | float
    vx: int | float
    vy: int | float
    radius: int | float

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.radius -= CIRCLE_RADIUS_10


class BasicEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 50, 50, 100)

        self.target: tuple[int, int] = self.rect.center
        """The target position to move to."""
        self.target_timer = TARGET_DELAY
        """The amount of frames to wait before changing the target."""

        self.circles: list[Circle] = []
        self.circle_timer = CIRCLE_SPAWN_DELAY

        self.sprite = pygame.surface.Surface((self.rect.w + CIRCLE_RADIUS * 4, self.rect.h + CIRCLE_RADIUS * 4))
        self.sprite_rect = self.sprite.get_rect()

        self.sub_sprite = pygame.surface.Surface((CIRCLE_RADIUS * 2 + 1, CIRCLE_RADIUS * 2 + 1))
        self.sub_sprite_rect = self.sub_sprite.get_rect()

    def _update_target(self, player: Player):
        if self.target_timer > 0:
            self.target_timer -= 1
            return

        self.target_timer = TARGET_DELAY

        x_diff = self.rect.centerx - player.rect.centerx
        y_diff = self.rect.centery - player.rect.centery

        x_diff_squared = x_diff * x_diff
        y_diff_squared = y_diff * y_diff

        distance_squared = x_diff_squared + y_diff_squared

        if distance_squared < 128 * 128:
            self.target = player.rect.center
        else:
            self.target = self.rect.x + random.randint(-128, 128), self.rect.y + random.randint(-128, 128)

    def _update_sprite(self):
        # Update the circles
        circles_len = len(self.circles)
        for i, circle in enumerate(self.circles[::-1]):
            i = circles_len - i - 1

            if circle.radius <= 0:
                del self.circles[i]

            circle.update()

        # Add a circle if necessary
        if self.circle_timer > 0:
            self.circle_timer -= 1
            return

        self.circle_timer = CIRCLE_SPAWN_DELAY

        self.circles.append(
            Circle(self.sprite.get_width() / 2, self.sprite.get_height() / 2,
                   random.random() - 0.5, random.random() - 0.5,
                   CIRCLE_RADIUS)
        )

    def update(self, player: Player, *_):
        self._update_target(player)
        self._update_sprite()

    def move(self, map_: Map):
        x_diff = self.target[0] - self.rect.centerx
        y_diff = self.target[1] - self.rect.centery

        x_diff_squared = x_diff * x_diff
        y_diff_squared = y_diff * y_diff

        distance_squared = x_diff_squared + y_diff_squared

        # If at target then do not move
        if distance_squared < TARGET_RADIUS_SQUARED:
            return

        x_move = x_diff
        if abs(x_diff) > 1:
            x_move = -1 if x_diff < 0 else 1

        y_move = y_diff
        if abs(y_diff) > 1:
            y_move = -1 if y_diff < 0 else 1

        # Normalise
        # vector_size = math.sqrt(x_move * x_move + y_move * y_move)
        #
        # print("Vector before", x_move, y_move)
        #
        # if vector_size != 0:
        #     x_move /= vector_size
        #     y_move /= vector_size
        #
        # print("Vector after", x_move, y_move)

        # Move to target
        self.move_x(map_, x_move)
        self.move_y(map_, y_move)

    def _render_sprite(self):
        self.sprite.fill((0, 0, 0))

        for circle in self.circles:
            self.sub_sprite.fill((0, 0, 0))
            pygame.draw.circle(self.sub_sprite, (10, 10, 10),
                               (self.sub_sprite.get_width() // 2, self.sub_sprite.get_height() // 2),
                               circle.radius)

            self.sub_sprite_rect.center = circle.x, circle.y
            self.sprite.blit(self.sub_sprite, self.sub_sprite_rect, special_flags=pygame.BLEND_RGB_ADD)

    def draw(self, camera: Camera):
        self.sprite_rect.center = self.rect.center

        if not camera.can_see(self.sprite_rect):
            return

        self._render_sprite()
        camera.convert_rect_to_camera_coordinates(self.sprite_rect)

        camera.window.blit(self.sprite, self.sprite_rect.topleft, special_flags=pygame.BLEND_RGB_SUB)
