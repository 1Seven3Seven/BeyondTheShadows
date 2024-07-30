import pygame

from .Helpers.CommonTypes import Number
from .PotionExploded import PotionExploded
from .UpgradeBase import UpgradeBase


class UpgradeLightRadius(UpgradeBase):
    SPRITE: pygame.Surface = pygame.Surface((25, 25))

    SPRITE.fill((127, 255, 127))

    def __init__(self, x: Number, y: Number):
        super().__init__(x, y, self.SPRITE)

    def effect(self) -> None:
        PotionExploded.increase_light_radius()
