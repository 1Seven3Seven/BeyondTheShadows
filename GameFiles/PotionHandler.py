from typing import Generator

from .Camera import Camera
from .Map import Map
from .Potion import Potion
from .Shadows import Shadows


class PotionHandler:
    def __init__(self):
        self.potions: list[Potion] = []

    def iter_potions_reverse(self) -> Generator[tuple[int, Potion], None, None]:
        for i in range(len(self.potions) - 1, -1, -1):
            yield i, self.potions[i]

    def update(self, map_: Map, enemies: list, shadows: Shadows) -> None:
        for i, potion in self.iter_potions_reverse():
            if potion.exploded:
                del self.potions[i]
                continue

            potion.update(map_, enemies, shadows)

    def draw(self, camera: Camera) -> None:
        for potion in self.potions:
            potion.draw(camera)
