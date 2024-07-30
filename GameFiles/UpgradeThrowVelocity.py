import pygame

from .Helpers.CommonTypes import Number
from .Player import Player
from .UpgradeBase import UpgradeBase


class UpgradeThrowVelocity(UpgradeBase):
    SPRITE: pygame.Surface = pygame.Surface((25, 25))

    SPRITE.fill((255, 127, 255))

    def __init__(self, x: Number, y: Number):
        super().__init__(x, y, self.SPRITE)

    def effect(self) -> None:
        Player.increase_throw_velocity()
