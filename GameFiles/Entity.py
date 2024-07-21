from abc import ABC, abstractmethod

import pygame

from .Map import Map, TILE_SIZE


class Entity(ABC):
    def __init__(self, x: float, y: float, width: float, height: float, health: int):
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)

        self.health = health

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        # Takes an unknown amount of arguments at this time
        raise NotImplementedError

    def _get_potential_collision_rectangles(self, map_: Map) -> list[pygame.Rect]:
        # Grab the tile we are currently in
        tile_x_base = self.rect.x // TILE_SIZE
        tile_y_base = self.rect.y // TILE_SIZE

        # Grab any rectangles from the map that we can collide with
        potential_collision_rectangles = []
        for x_diff in range(-1, 2):
            tile_x = tile_x_base + x_diff

            if tile_x < 0:
                continue
            if tile_x >= map_.width:
                continue

            for y_diff in range(-1, 2):
                tile_y = tile_y_base + y_diff

                if tile_y < 0:
                    continue
                if tile_y >= map_.height:
                    continue

                tile_str = f"{tile_x},{tile_y}"

                if tile_str in map_.tiles:
                    potential_collision_rectangles.append(map_.tiles[tile_str])

        return potential_collision_rectangles

    def move_x(self, map_: Map, x: int | float) -> None:
        """
        Move the entity by given amount.
        Checks for and resolves collisions with the map tiles.
        """

        if x == 0:
            return

        self.rect.x += x

        for rect in self._get_potential_collision_rectangles(map_):
            if self.rect.colliderect(rect):
                if x > 0:
                    self.rect.right = rect.left
                else:
                    self.rect.left = rect.right

    def move_y(self, map_: Map, y: int | float) -> None:
        """
        Move the entity by given amount.
        Checks for and resolves collisions with the map tiles.
        """

        if y == 0:
            return

        self.rect.y += y

        for rect in self._get_potential_collision_rectangles(map_):
            if self.rect.colliderect(rect):
                if self.rect.colliderect(rect):
                    if y > 0:
                        self.rect.bottom = rect.top
                    else:
                        self.rect.top = rect.bottom

    @abstractmethod
    def move(self, *args, **kwargs) -> None:
        # Takes an unknown amount of arguments at this time
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        raise NotImplementedError
