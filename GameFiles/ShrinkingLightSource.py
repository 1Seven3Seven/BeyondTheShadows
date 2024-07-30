from .Helpers.CommonTypes import Number
from .UpdatingLightSource import UpdatingLightSource


class ShrinkingLightSource(UpdatingLightSource):
    def __init__(self, x: Number, y: Number, brightness: int, radius: int, lifespan: int):
        super().__init__(x, y, brightness, radius)

        self.max_radius = self.radius

        self.max_lifespan: int = lifespan
        self.lifespan: int = lifespan

    def update(self) -> None:
        self.lifespan -= 1
        interpolate = self.lifespan / self.max_lifespan
        self.radius = int(interpolate * self.max_radius + (1 - interpolate) * 16)

        if self.lifespan <= 0:
            self.to_remove = True
