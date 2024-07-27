import pygame

from .Camera import Camera


class Particle:
    def __init__(self, x: int | float, y: int | float,
                 vx: int | float, vy: int | float,
                 lifespan: int, sprite: pygame.Surface):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.lifespan = lifespan
        self.sprite = sprite
        self.sprite_rect = sprite.get_rect()

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy

        self.lifespan -= 1

    def draw(self, camera: Camera) -> None:
        if not camera.can_see(self.sprite_rect):
            return

        camera.convert_rect_to_camera_coordinates(self.sprite_rect)
        camera.window.blit(self.sprite, self.sprite_rect)
