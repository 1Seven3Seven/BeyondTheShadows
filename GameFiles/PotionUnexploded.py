import math

import pygame

from .Camera import Camera
from .Entity import Entity
from .LightSource import LightSource
from .Map import Map
from .ParticleHandler import ParticleHandler
from .Shadows import Shadows


class PotionUnexploded:
    SIZE = 10 * 1.5
    """The size of the square hitbox given a circle of radius 10 as the sprite."""

    DAMAGE: int = 10  # I think that 10 as a base and 50 as max is good
    """The damage done upon direct contact with an enemy."""
    MAX_DAMAGE: int = 50

    @classmethod
    def increase_damage(cls, increase_by: int = 10) -> bool:
        """
        Attempts to increase the damage.
        If at max, then True is returned, else false
        """

        cls.DAMAGE += increase_by

        if cls.DAMAGE > cls.MAX_DAMAGE:
            cls.DAMAGE = cls.MAX_DAMAGE
            return True
        return False

    def __init__(self, x: int | float, y: int | float, angle: float, velocity: int | float, shadows: Shadows):
        """
        :param x: The initial x position of the potion.
        :param y: The initial y position of the potion.
        :param angle: The angle the potion is thrown at in radians.
        :param velocity: The velocity the position is thrown at.
        """

        self.x = x
        self.y = y

        self.rect: pygame.Rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)

        self.angle = angle
        self.velocity = velocity

        self.vx = math.cos(angle)
        self.vy = math.sin(angle)

        self.exploded: bool = False
        """If true, then this potion has exploded and should be removed."""

        self.light_source: LightSource | None = LightSource(
            self.x, self.y, 255, 48
        )

        self.damage: int = self.DAMAGE

    def explode(self, shadows: Shadows) -> None:
        self.exploded = True
        shadows.remove_light_source(self.light_source)

    def _move_and_update_light_source(self, shadows: Shadows) -> None:
        self.x += self.vx * self.velocity
        self.y += self.vy * self.velocity
        self.velocity -= 1

        # Update the light source position
        shadows.remove_light_source(self.light_source)
        self.light_source.x = self.x
        self.light_source.y = self.y
        shadows.add_light_source(self.light_source)

    def update(self, map_: Map, enemies: list[Entity], shadows: Shadows, particle_handler: ParticleHandler) -> None:
        # Should not occur, but if the potion has collided with something, then do not update
        if self.exploded:
            return

        # If no longer moving
        if self.velocity <= 0:
            self.explode(shadows)
            return

        self._move_and_update_light_source(shadows)

        # Position the collision rectangle
        self.rect.center = self.x, self.y

        # Check for collision with enemies
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.deal_damage(self.damage)
                self.explode(shadows)

        # Check for collisions with tiles
        for rect in map_.surrounding_tiles(self.x, self.y):
            if rect.collidepoint(self.x, self.y):
                self.explode(shadows)

    def draw(self, camera: Camera) -> None:
        # ToDo: draw the potion
        # A glowing circle will be good enough

        display_coords = camera.coordinates_to_display_coordinates((self.x, self.y))

        pygame.draw.circle(camera.window, (0, 255, 0), display_coords, 10)
