from abc import ABC, abstractmethod

import pygame

from .Camera import Camera
from .Map import Map


class Entity(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, health: int):
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)

        self.health = health

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        # Takes an unknown amount of arguments at this time
        raise NotImplementedError

    def move_x(self, map_: Map, x: int | float) -> None:
        """
        Move the entity by given amount.
        Checks for and resolves collisions with the map tiles.
        """

        if x == 0:
            return

        self.rect.x += x

        # for rect in map_.surrounding_tiles(self.rect.centerx, self.rect.centery):
        for rect in map_.tiles_touching(self.rect):
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

        # for rect in map_.surrounding_tiles(self.rect.centerx, self.rect.centery):
        for rect in map_.tiles_touching(self.rect):
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
    def draw(self, camera: Camera) -> None:
        raise NotImplementedError

    def deal_damage(self, damage: int) -> bool:
        """
        Deals the given damage to the entity.
        Returns if the entity has died.
        """

        self.health -= damage
        if self.health <= 0:
            return True
        return False
