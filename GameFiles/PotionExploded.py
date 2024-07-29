import math
import random

import pygame

from .Camera import Camera
from .Entity import Entity
from .LightSource import LightSource
from .ParticleHandler import ParticleHandler
from .Shadows import Shadows


class PotionExploded:
    # Light source stats
    BRIGHTNESS: int = 300
    LIGHT_RADIUS: int = 80  # I like 80 as a start, and 128 as the max
    LIGHT_RADIUS_SQRT_2 = int(LIGHT_RADIUS * math.sqrt(2))

    PARTICLE_SPAWN_TIME: int = 5
    """The delay in frames between spawning particles."""
    PARTICLE_LIFESPAN: int = 20

    HEALTH: int = 100  # 100 as base and 200 as max
    """
    The 'health' of the potion.
    An exploded potions 'health' gets drained when it causes damage to enemies.
    """

    DAMAGE: int = 1
    """
    The amount of damage done every damage frame.
    """

    DAMAGE_FRAME: int = 6

    WEAR_OUT_FRAME: int = 18  # Lasts 30 seconds if nothing happens and 60 at max health

    # Note the max damage delt via exposure is HEALTH * DAMAGE

    @classmethod
    def increase_light_radius(cls, increase_by: int = 16) -> None:
        cls.LIGHT_RADIUS += increase_by
        cls.LIGHT_RADIUS_SQRT_2 = cls.LIGHT_RADIUS * math.sqrt(2)

    @classmethod
    def increase_health(cls, increase_by: int = 50) -> None:
        cls.HEALTH += increase_by

    def __init__(self, x: int | float, y: int | float, shadows: Shadows, update_offset: int = 0):
        self.x = x
        self.y = y

        self.rect: pygame.Rect = pygame.Rect(0, 0, self.LIGHT_RADIUS_SQRT_2, self.LIGHT_RADIUS_SQRT_2)
        self.rect.center = self.x, self.y

        self.light_source: LightSource = LightSource(
            x, y, self.BRIGHTNESS, self.LIGHT_RADIUS
        )
        shadows.add_light_source(self.light_source)

        self.particle_spawn_timer: int = self.PARTICLE_SPAWN_TIME

        self.health: int = self.HEALTH

        self.damage: int = self.DAMAGE
        self.damage_timer: int = 0 + update_offset

        self.wear_out_timer: int = self.WEAR_OUT_FRAME

        self.double_exploded: bool = False
        """If double exploded, then this exploded potion should be removed."""

    def _spawn_particles(self, particle_handler: ParticleHandler) -> None:
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

    def _damage_enemies(self, particle_handler: ParticleHandler, enemies: list[Entity]) -> bool:
        """
        Returns true of the potion has double exploded.
        """

        if self.damage_timer >= 0:
            self.damage_timer -= 1
            return False

        self.damage_timer = self.DAMAGE_FRAME

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.deal_damage(self.damage)
                self.health -= 1

                print(f"Health: {self.health}")

                if self.health <= 0:
                    self._double_explode(particle_handler)
                    return True

        return False

    def _double_explode(self, particle_handler: ParticleHandler) -> None:
        # ToDo: explode with style, and particles
        self.double_exploded = True

    def _wear_out(self) -> bool:
        """
        Returns true if the potion has worn out.
        """

        if self.wear_out_timer >= 0:
            self.wear_out_timer -= 1
            return False

        self.wear_out_timer = self.WEAR_OUT_FRAME

        self.health -= 1

        if self.health <= 0:
            self.double_exploded = True
            return True
        return False

    def update(self, particle_handler: ParticleHandler, enemies: list[Entity]) -> None:
        # Should not occur, do thing if to be deleted
        if self.double_exploded:
            return

        if self._damage_enemies(particle_handler, enemies):
            return

        if self._wear_out():
            return

        self._spawn_particles(particle_handler)

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        display_coords = camera.coordinates_to_display_coordinates(self.rect.center)

        pygame.draw.circle(camera.window, (255, 127, 0), display_coords, 10)

        display_rect = self.rect.copy()
        camera.convert_rect_to_camera_coordinates(display_rect)
        pygame.draw.rect(camera.window, (255, 255, 255), display_rect, 1)
