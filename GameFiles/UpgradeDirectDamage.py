import pygame

from .Helpers.CommonTypes import Number
from .PotionUnexploded import PotionUnexploded
from .UpgradeBase import UpgradeBase


class UpgradeDirectDamage(UpgradeBase):
    SPRITE: pygame.Surface = pygame.Surface((25, 25))

    SPRITE.fill((255, 127, 127))

    def __init__(self, x: Number, y: Number):
        super().__init__(x, y, self.SPRITE)

    def effect(self) -> None:
        PotionUnexploded.increase_damage()
