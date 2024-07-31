from abc import ABC, abstractmethod

from .Camera import Camera
from .Entity import Entity
from .Helpers.CommonTypes import Coordinates
from .Map import Map
from .ParticleHandler import ParticleHandler
from .Player import Player
from .PotionHandler import PotionHandler


class Enemy(Entity, ABC):
    @abstractmethod
    def update(self, player: Player, map_: Map, particle_handler: ParticleHandler,
               potion_handler: PotionHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    def move(self, map_: Map) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, camera: Camera) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_room_id(self, room_id: int, map_: Map) -> None:
        """
        An enemy may be constrained to a room.
        This is used to tell the entity of such a thing.
        """

        raise NotImplementedError

    @abstractmethod
    def set_center(self, coords: Coordinates):
        raise NotImplementedError
