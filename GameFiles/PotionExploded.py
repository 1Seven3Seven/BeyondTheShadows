import math
import random

import pygame

from .Camera import Camera
from .Entity import Entity
from .LightSource import LightSource
from .ParticleHandler import ParticleHandler
from .Shadows import Shadows
from .ShrinkingLightSource import ShrinkingLightSource


class PotionExploded:
    # Light source stats
    BRIGHTNESS: int = 300
    START_LIGHT_RADIUS: int = 80
    LIGHT_RADIUS: int = START_LIGHT_RADIUS  # I like 80 as a start, and 128 as the max
    MAX_LIGHT_RADIUS: int = 128
    LIGHT_RADIUS_SQRT_2 = int(LIGHT_RADIUS * math.sqrt(2))

    PARTICLE_SPAWN_TIME: int = 5
    """The delay in frames between spawning particles."""
    PARTICLE_LIFESPAN: int = 20

    START_HEALTH: int = 100
    HEALTH: int = 100  # 100 as base and 200 as max
    """
    The 'health' of the potion.
    An exploded potions 'health' gets drained when it causes damage to enemies.
    """
    MAX_HEALTH: int = 200

    DAMAGE: int = 1
    """
    The amount of damage done every damage frame.
    """

    DAMAGE_FRAME: int = 6

    WEAR_OUT_FRAME: int = 18  # Lasts 30 seconds if nothing happens and 60 at max health

    NUM_DOUBLE_EXPLODE_PARTICLES = 10

    # Note the max damage delt via exposure is HEALTH * DAMAGE

    @classmethod
    def reset_upgrades(cls) -> None:
        cls.LIGHT_RADIUS = cls.START_LIGHT_RADIUS
        cls.HEALTH = cls.START_HEALTH

    @classmethod
    def increase_light_radius(cls, increase_by: int = 16) -> bool:
        """
        Attempts to increase the light radius of the potion.
        If at max radius, then True is returned.
        """

        cls.LIGHT_RADIUS += increase_by

        if cls.LIGHT_RADIUS > cls.MAX_LIGHT_RADIUS:
            cls.LIGHT_RADIUS = cls.MAX_LIGHT_RADIUS
            cls.LIGHT_RADIUS_SQRT_2 = cls.LIGHT_RADIUS * math.sqrt(2)
            return True

        cls.LIGHT_RADIUS_SQRT_2 = cls.LIGHT_RADIUS * math.sqrt(2)
        return False

    @classmethod
    def increase_health(cls, increase_by: int = 50) -> bool:
        """
        Attempts to increase the health of the potion.
        If at max health, then True is returned.
        """

        cls.HEALTH += increase_by

        if cls.HEALTH >= cls.MAX_HEALTH:
            cls.HEALTH = cls.MAX_HEALTH
            return True
        return False

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

    def _damage_enemies(self, enemies: list[Entity]) -> bool:
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

                if self.health <= 0:
                    return True

        return False

    def _double_explode(self, shadows: Shadows, particle_handler: ParticleHandler) -> None:
        self.double_exploded = True

        shadows.add_updating_light_source(
            ShrinkingLightSource(self.x, self.y, self.BRIGHTNESS, self.LIGHT_RADIUS, 30),
        )

        for _ in range(self.NUM_DOUBLE_EXPLODE_PARTICLES):
            velocity = random.randint(1, 3)
            angle = random.uniform(0, 2 * math.pi)

            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity

            particle_handler.create_particle(
                "double exploded potion",
                self.x, self.y,
                vx, vy,
                random.randint(10, 20)
            )

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

    def update(self, shadows: Shadows, particle_handler: ParticleHandler, enemies: list[Entity]) -> None:
        # Should not occur, do thing if to be deleted
        if self.double_exploded:
            return

        if self._damage_enemies(enemies):
            self._double_explode(shadows, particle_handler)
            return

        if self._wear_out():
            self._double_explode(shadows, particle_handler)
            return

        self._spawn_particles(particle_handler)

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.rect):
            return

        display_coords = camera.coordinates_to_display_coordinates(self.rect.center)

        pygame.draw.circle(camera.window, (255, 127, 0), display_coords, 10)

        # display_rect = self.rect.copy()
        # camera.convert_rect_to_camera_coordinates(display_rect)
        # pygame.draw.rect(camera.window, (255, 255, 255), display_rect, 1)
