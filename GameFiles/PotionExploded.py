import math
import random

import pygame

from .Camera import Camera
from .LightSource import LightSource
from .ParticleHandler import ParticleHandler
from .Shadows import Shadows


class PotionExploded:
    # Light source stats
    BRIGHTNESS: int = 300
    LIGHT_RADIUS: int = 128

    SIZE: int = 6
    """The size of the collision rectangle. Should be even."""
    SIZE_2: int = int(SIZE // 2)

    PARTICLE_SPAWN_TIME: int = 5
    """The delay in frames between spawning particles."""
    PARTICLE_LIFESPAN: int = 20

    def __init__(self, x: int | float, y: int | float, shadows: Shadows):
        self.x = x
        self.y = y

        self.rect: pygame.Rect = pygame.Rect(self.x - self.SIZE_2, self.y - self.SIZE_2, self.SIZE, self.SIZE)

        self.light_source: LightSource = LightSource(
            x, y, self.BRIGHTNESS, self.LIGHT_RADIUS
        )
        shadows.add_light_source(self.light_source)

        self.timer: int = self.PARTICLE_SPAWN_TIME

    def update(self, particle_handler: ParticleHandler) -> None:
        if self.timer >= 0:
            self.timer -= 1
            return

        self.timer = self.PARTICLE_SPAWN_TIME

        angle = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle)
        vy = math.sin(angle)

        particle_handler.create_particle(
            "test",
            self.x, self.y,
            vx, vy,
            self.PARTICLE_LIFESPAN
        )

    def draw(self, camera: Camera) -> None:
        display_coords = camera.coordinates_to_display_coordinates(self.rect.center)

        pygame.draw.circle(camera.window, (255, 127, 0), display_coords, 10)
