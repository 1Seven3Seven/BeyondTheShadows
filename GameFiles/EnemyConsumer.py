from .Camera import Camera
from .Enemy import Enemy
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class EnemyConsumer(Enemy):
    def update(self, player: Player, map_: Map, potion_handler: PotionHandler) -> None:
        pass

    def move(self, map_: Map) -> None:
        pass

    def draw(self, camera: Camera) -> None:
        pass
