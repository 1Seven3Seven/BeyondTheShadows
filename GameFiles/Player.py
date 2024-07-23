import pygame

from .Map import Map
from .Entity import Entity


class Player(Entity):
    ATTACK_DELAY = 60

    def __init__(self):
        super().__init__(300, 300, 50, 50, 100)

        self.attack_delay = self.ATTACK_DELAY

    def update(self):
        if self.attack_delay > 0:
            self.attack_delay -= 1

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

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
