from abc import ABC, abstractmethod

import pygame

from .Camera import Camera
from .Helpers.CommonTypes import Number, Coordinates
from .Player import Player


class UpgradeBase(ABC):
    def __init__(self, x: Number, y: Number, sprite: pygame.Surface):
        """
        The sprite given should be 25 by 25 pixels.
        """

        self.position: Coordinates = x, y

        self.rect: pygame.Rect = pygame.Rect(0, 0, 25, 25)

        self.sprite: pygame.Surface = sprite

        self.used: bool = False
        """If the player has used this upgrade, it is to be removed."""

    def update(self, player: Player) -> None:
        self.rect.center = self.position

        if self.rect.colliderect(player.rect):
            self.effect()
            self.used = True

    @abstractmethod
    def effect(self) -> None:
        """
        Causes the upgrade to cause an effect.
        """

        raise NotImplementedError

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        camera.convert_rect_to_camera_coordinates(self.rect)

        camera.window.blit(self.sprite, self.rect)
