from .Camera import Camera
from .Enemy import Enemy
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class EnemyDarkling(Enemy):
    def update(self, player: Player, map_: Map, potion_handler: PotionHandler) -> None:
        pass

    def move(self, map_: Map) -> None:
        pass

    def draw(self, camera: Camera) -> None:
        pass

    def set_room_id(self, room_id: int, map_: Map) -> None:
        pass

    def set_center(self, coords: Coordinates):
        pass
