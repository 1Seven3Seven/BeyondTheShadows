import pygame

from . import Map
from .Entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__(300, 300, 50, 50, 100)

    def update(self, *args, **kwargs):
        pass

    def move(self, keys: pygame.key.ScancodeWrapper, map_: Map):
        y_movement = 0

        if keys[pygame.K_UP]:
            y_movement -= 3
        if keys[pygame.K_DOWN]:
            y_movement += 3

        self.move_y(map_, y_movement)

        x_movement = 0

        if keys[pygame.K_LEFT]:
            x_movement -= 3
        if keys[pygame.K_RIGHT]:
            x_movement += 3

        self.move_x(map_, x_movement)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
