from .Camera import Camera
from .Enemy import Enemy
from .Map import Map
from .Player import Player
from .PotionHandler import PotionHandler


class EnemyHandler:
    def __init__(self):
        self.enemies: list[Enemy] = []

    def update_move_and_draw_enemies(self,
                                     player: Player,
                                     map_: Map,
                                     potion_handler: PotionHandler,
                                     camera: Camera) -> None:
        for enemy in self.enemies:
            enemy.update(player, map_, potion_handler)
            enemy.move(map_)
            enemy.draw(camera)
