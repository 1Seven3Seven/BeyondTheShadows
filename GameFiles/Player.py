import math
import random

import pygame

from .Camera import Camera
from .Entity import Entity
from .Helpers import MouseSate
from .LightSource import LightSource
from .Map import Map
from .MapData import MapData
from .ParticleHandler import ParticleHandler
from .PotionHandler import PotionHandler
from .Shadows import Shadows
from .ShrinkingLightSource import ShrinkingLightSource


class Player(Entity):
    WIDTH: int = 50
    HEIGHT: int = 50

    HEALTH: int = 50
    """The initial starting health of the player."""

    ATTACK_DELAY: int = 45
    THROW_VELOCITY: int = 12  # I like a max of 18
    MAX_THROW_VELOCITY: int = 18

    # About the light the player casts
    BRIGHTNESS: int = 255
    LIGHT_RADIUS: int = 64

    DEATH_TIMER: int = 90
    """How long the death animation lasts in frames."""

    INITIAL_DEATH_NUM_PARTICLES: int = 30

    @classmethod
    def increase_throw_velocity(cls, increase_by: int = 2):
        cls.THROW_VELOCITY += increase_by

        if cls.THROW_VELOCITY > cls.MAX_THROW_VELOCITY:
            cls.THROW_VELOCITY = cls.MAX_THROW_VELOCITY
            return True
        return False

    def __init__(self):
        super().__init__(0, 0, self.WIDTH, self.HEIGHT, self.HEALTH)

        self.attack_delay = self.ATTACK_DELAY
        self.display_rect: pygame.Rect = self.rect.copy()

        self.light_source: LightSource = LightSource(self.rect.centerx, self.rect.centerx,
                                                     self.BRIGHTNESS, self.LIGHT_RADIUS)

        self.i_am_dead: bool = False
        self.death_animation_finished: bool = False
        self.death_timer: int = self.DEATH_TIMER

    def setup_from(self, map_data: MapData, map_: Map):
        self.health = self.HEALTH
        self.attack_delay = self.ATTACK_DELAY

        self.rect.center = (
            map_data.player_spawn[0] * map_.TILE_SIZE + map_.TILE_SIZE_2,
            map_data.player_spawn[1] * map_.TILE_SIZE + map_.TILE_SIZE_2
        )

        # ALIVE, WOO!
        self.i_am_dead = False
        self.death_animation_finished = False
        self.death_timer: int = self.DEATH_TIMER

    def _update_attack(self, keys: pygame.key.ScancodeWrapper, mouse_state: MouseSate,
                       potion_handler: PotionHandler, shadows: Shadows):
        if self.attack_delay > 0:
            self.attack_delay -= 1
            return

        if not keys[pygame.K_SPACE] and not mouse_state["buttons"][0]:
            return

        # Get the angle from the player center to the mouse
        angle = math.atan2(mouse_state["position"][1] - self.display_rect.centery,
                           mouse_state["position"][0] - self.display_rect.centerx)

        # Create a potion thrown in that direction
        potion_handler.create_potion(self.rect.center, angle, self.THROW_VELOCITY, shadows)

        self.attack_delay = self.ATTACK_DELAY

    def _update_light_source(self, shadows: Shadows) -> None:
        shadows.remove_light_source(self.light_source)

        self.light_source.x = self.rect.centerx
        self.light_source.y = self.rect.centery

        shadows.add_light_source(self.light_source)

    def _begin_death(self, particle_handler: ParticleHandler, shadows: Shadows) -> None:
        if self.i_am_dead:
            return

        self.i_am_dead = True

        shadows.remove_light_source(self.light_source)
        shadows.add_updating_light_source(
            ShrinkingLightSource(self.rect.centerx, self.rect.centery,
                                 self.BRIGHTNESS, self.LIGHT_RADIUS,
                                 self.DEATH_TIMER)
        )

        for _ in range(self.INITIAL_DEATH_NUM_PARTICLES):
            velocity = random.randint(1, 5)
            angle = random.uniform(0, 2 * math.pi)

            vx = math.cos(angle) * velocity
            vy = math.sin(angle) * velocity

            particle_handler.create_particle(
                "player death",
                self.rect.centerx, self.rect.centery,
                vx, vy,
                random.randint(5, 30)
            )

    def _update_death(self, particle_handler: ParticleHandler, shadows: Shadows) -> None:
        if self.death_animation_finished:
            return

        self._begin_death(particle_handler, shadows)

        # velocity = random.randint(1, 2)
        # angle = random.uniform(0, 2 * math.pi)
        #
        # vx = math.cos(angle) * velocity
        # vy = math.sin(angle) * velocity
        #
        # particle_handler.create_particle(
        #     "player death 2",
        #     self.rect.centerx, self.rect.centery,
        #     vx, vy,
        #     random.randint(5, 20)
        # )

        if self.death_timer > 0:
            self.death_timer -= 1
            return

        self.death_animation_finished = True

    def update(self, keys: pygame.key.ScancodeWrapper, mouse_state: MouseSate,
               particle_handler: ParticleHandler, potion_handler: PotionHandler, shadows: Shadows):
        if self.health > 0:
            self._update_attack(keys, mouse_state, potion_handler, shadows)
            self._update_light_source(shadows)
        else:
            self._update_death(particle_handler, shadows)

    def move(self, keys: pygame.key.ScancodeWrapper, map_: Map):
        if self.i_am_dead:
            return

        y_movement = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y_movement -= 3
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y_movement += 3

        self.move_y(map_, y_movement)

        x_movement = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_movement -= 3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_movement += 3

        self.move_x(map_, x_movement)

    def draw(self, camera: Camera):
        # No need to draw if, well I am dead
        if self.i_am_dead:
            return

        if not camera.can_see(self.rect):
            return

        self.display_rect.topleft = self.rect.topleft
        camera.convert_rect_to_camera_coordinates(self.display_rect)

        pygame.draw.rect(camera.window, (255, 255, 255), self.display_rect)
