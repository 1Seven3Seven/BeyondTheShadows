import pygame

from .Camera import Camera
from .LightSource import LightSource
from .Shadows import Shadows


class PotionExploded:
    # Light source stats
    BRIGHTNESS: int = 300
    LIGHT_RADIUS: int = 128

    SIZE: int = 6
    """The size of the collision rectangle. Should be even."""
    SIZE_2: int = int(SIZE // 2)

    def __init__(self, x: int | float, y: int | float, shadows: Shadows):
        self.x = x
        self.y = y

        self.rect: pygame.Rect = pygame.Rect(self.x - self.SIZE_2, self.y - self.SIZE_2, self.SIZE, self.SIZE)

        self.light_source: LightSource = LightSource(
            x, y, self.BRIGHTNESS, self.LIGHT_RADIUS
        )
        shadows.add_light_source(self.light_source)

    def update(self) -> None:
        pass

    def draw(self, camera: Camera) -> None:
        display_coords = camera.coordinates_to_display_coordinates(self.rect.center)

        pygame.draw.circle(camera.window, (255, 127, 0), display_coords, 10)
