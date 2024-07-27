import math

import pygame

from .Camera import Camera
from .LightSource import LightSource
from .Map import Map
from .ParticleHandler import ParticleHandler
from .Shadows import Shadows


class PotionUnexploded:
    BRIGHTNESS: int = 300
    RADIUS: int = 128

    def __init__(self, x: int | float, y: int | float, angle: float, velocity: int | float, shadows: Shadows):
        """
        :param x: The initial x position of the potion.
        :param y: The initial y position of the potion.
        :param angle: The angle the potion is thrown at in radians.
        :param velocity: The velocity the position is thrown at.
        """

        self.x = x
        self.y = y

        self.angle = angle
        self.velocity = velocity

        self.vx = math.cos(angle)
        self.vy = math.sin(angle)

        self.exploded: bool = False
        """If true, then this potion has exploded and should be removed."""

        self.light_source: LightSource | None = LightSource(
            self.x, self.y, 255, 48
        )
        shadows.add_light_source(self.light_source)

    def explode(self, shadows: Shadows) -> None:
        self.exploded = True
        shadows.remove_light_source(self.light_source)

    def update(self, map_: Map, enemies: list, shadows: Shadows, particle_handler: ParticleHandler) -> None:
        # ToDo: add collision with enemies

        # Should not occur, but if the potion has collided with something, then do not update
        if self.exploded:
            return

        # If no longer moving
        if self.velocity == 0:
            self.explode(shadows)
            return

        # If moving, then move
        self.x += self.vx * self.velocity
        self.y += self.vy * self.velocity
        self.velocity -= 1

        shadows.remove_light_source(self.light_source)

        self.light_source.x = self.x
        self.light_source.y = self.y

        shadows.add_light_source(self.light_source)

        # Check for collisions with tiles
        for rect in map_.surrounding_tiles(self.x, self.y):
            if rect.collidepoint(self.x, self.y):
                self.explode(shadows)

    def draw(self, camera: Camera) -> None:
        # ToDo: draw the potion
        # A glowing circle will be good enough

        display_coords = camera.coordinates_to_display_coordinates((self.x, self.y))

        pygame.draw.circle(camera.window, (0, 255, 0), display_coords, 10)
