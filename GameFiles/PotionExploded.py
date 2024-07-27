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

    SIZE: int = 20
    """The size of the collision rectangle. Should be even."""
    SIZE_2: int = int(SIZE // 2)
    SIZE_4: int = int(SIZE // 4)

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

        self.particle_spawn_timer: int = self.PARTICLE_SPAWN_TIME
        self.timer: int = 0

    def update(self, particle_handler: ParticleHandler) -> None:
        self.timer += 1

        if self.particle_spawn_timer >= 0:
            self.particle_spawn_timer -= 1
            return

        self.particle_spawn_timer = self.PARTICLE_SPAWN_TIME

        angle = random.uniform(0, 2 * math.pi)
        vx = math.cos(angle) / 10
        vy = math.sin(angle) / 10

        particle_handler.create_particle(
            "exploded potion",
            self.x, self.y,
            vx, vy,
            self.PARTICLE_LIFESPAN
        )

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        display_coords = camera.coordinates_to_display_coordinates(self.rect.center)

        radius = self.SIZE_4 + self.SIZE_4 * (1 + math.cos(self.timer / 250 * math.pi * 2)) / 2

        pygame.draw.circle(camera.window, (255, 127, 0), display_coords, radius)

        display_rect = self.rect.copy()
        camera.convert_rect_to_camera_coordinates(display_rect)
        pygame.draw.rect(camera.window, (255, 255, 255), display_rect, 1)
