from abc import ABC, abstractmethod

from . import Camera
from .Entity import Entity
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class Enemy(Entity, ABC):
    @abstractmethod
    def update(self, player: Player, map_: Map, potion_handler: PotionHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def move(self, map_: Map) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        raise NotImplementedError
