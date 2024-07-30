from abc import ABC, abstractmethod

from .Helpers.CommonTypes import Number
from .LightSource import LightSource


class UpdatingLightSource(LightSource, ABC):
    def __init__(self, x: Number, y: Number, brightness: int, radius: int):
        super().__init__(x, y, brightness, radius)

        self.to_remove: bool = False
        """To be set when this light source is to be removed."""

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError
