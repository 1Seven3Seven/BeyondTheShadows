import math
import random

import pygame

from .Helpers.CommonTypes import Number
from .ParticleHandler import ParticleHandler
from .Player import Player
from .UpgradeBase import UpgradeBase


class UpgradeThrowVelocity(UpgradeBase):
    SPRITE: pygame.Surface = pygame.Surface((25, 25))

    SPRITE.fill((127, 255, 127))

    def __init__(self, x: Number, y: Number):
        super().__init__(x, y, self.SPRITE)

    def effect(self, particle_handler: ParticleHandler) -> None:
        Player.increase_throw_velocity()

        for _ in range(50):
            velocity = random.uniform(0.1, 2)
            angle = random.uniform(0, 2 * math.pi)

            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity

            particle_handler.create_particle(
                "throw velocity",
                self.rect.centerx, self.rect.centery,
                vx, vy,
                random.randint(5, 30)
            )
