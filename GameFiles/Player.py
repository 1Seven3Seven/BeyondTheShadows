import math

import pygame

from .Camera import Camera
from .Entity import Entity
from .Helpers import MouseSate
from .Map import Map
from .Potion import Potion
from .PotionHandler import PotionHandler


class Player(Entity):
    ATTACK_DELAY = 30
    THROW_VELOCITY = 12

    def __init__(self):
        super().__init__(300, 300, 50, 50, 100)

        self.attack_delay = self.ATTACK_DELAY
        self.display_rect: pygame.Rect = self.rect.copy()

    def _update_attack(self, keys: pygame.key.ScancodeWrapper, mouse_state: MouseSate, potion_handler: PotionHandler):
        if self.attack_delay > 0:
            self.attack_delay -= 1
            return

        if not keys[pygame.K_SPACE] and not mouse_state["buttons"][0]:
            return

        # Get the angle from the player center to the mouse
        angle = math.atan2(mouse_state["position"][1] - self.display_rect.centery,
                           mouse_state["position"][0] - self.display_rect.centerx)

        # Create a potion thrown in that direction
        potion_handler.potions.append(
            Potion(self.rect.centerx, self.rect.centery, angle, self.THROW_VELOCITY)
        )

        self.attack_delay = self.ATTACK_DELAY

    def update(self, keys: pygame.key.ScancodeWrapper, mouse_state: MouseSate, potion_handler: PotionHandler):
        self._update_attack(keys, mouse_state, potion_handler)

    def move(self, keys: pygame.key.ScancodeWrapper, map_: Map):
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
        if not camera.can_see(self.rect):
            return

        self.display_rect.topleft = self.rect.topleft
        camera.convert_rect_to_camera_coordinates(self.display_rect)

        pygame.draw.rect(camera.window, (255, 255, 255), self.display_rect)
