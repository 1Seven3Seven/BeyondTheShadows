from typing import Generator

from .Camera import Camera
from .Map import Map
from .ParticleHandler import ParticleHandler
from .PotionExploded import PotionExploded
from .PotionUnexploded import PotionUnexploded
from .Shadows import Shadows


class PotionHandler:
    def __init__(self):
        self.unexploded_potions: list[PotionUnexploded] = []
        self.exploded_potions: list[PotionExploded] = []

    @staticmethod
    def iter_potions_reverse(potion_list: list[PotionUnexploded | PotionExploded]) \
            -> Generator[tuple[int, PotionUnexploded | PotionExploded], None, None]:
        for i in range(len(potion_list) - 1, -1, -1):
            yield i, potion_list[i]

    def update(self, map_: Map, enemies: list, shadows: Shadows, particle_handler: ParticleHandler) -> None:
        potion_unexploded: PotionUnexploded
        for i, potion_unexploded in self.iter_potions_reverse(self.unexploded_potions):
            if potion_unexploded.exploded:
                self._create_potion_exploded(potion_unexploded, shadows)

                del self.unexploded_potions[i]
                continue

            potion_unexploded.update(map_, enemies, shadows, particle_handler)

        potion_exploded: PotionExploded
        for i, potion_exploded in self.iter_potions_reverse(self.exploded_potions):
            potion_exploded.update(particle_handler)

    def draw(self, camera: Camera) -> None:
        for potion in self.unexploded_potions:
            potion.draw(camera)

        for potion in self.exploded_potions:
            potion.draw(camera)

    def create_potion(self, position: tuple[int | float, int | float],
                      angle: float, velocity: int | float,
                      shadows: Shadows) -> None:
        self.unexploded_potions.append(
            PotionUnexploded(position[0], position[1], angle, velocity, shadows)
        )

    def _create_potion_exploded(self, potion: PotionUnexploded, shadows: Shadows) -> None:
        self.exploded_potions.append(
            PotionExploded(potion.x, potion.y, shadows)
        )
