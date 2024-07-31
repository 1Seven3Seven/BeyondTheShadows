import math
import random

import pygame

from .Helpers.CommonTypes import Number
from .ParticleHandler import ParticleHandler
from .PotionExploded import PotionExploded
from .UpgradeBase import UpgradeBase


class UpgradeLightRadius(UpgradeBase):
    SPRITE: pygame.Surface = pygame.Surface((25, 25))

    SPRITE.fill((255, 255, 127))

    def __init__(self, x: Number, y: Number):
        super().__init__(x, y, self.SPRITE)

    def effect(self, particle_handler: ParticleHandler) -> None:
        PotionExploded.increase_light_radius()

        for _ in range(50):
            velocity = random.uniform(0.1, 2)
            angle = random.uniform(0, 2 * math.pi)

            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity

            particle_handler.create_particle(
                "light radius",
                self.rect.centerx, self.rect.centery,
                vx, vy,
                random.randint(5, 30)
            )
