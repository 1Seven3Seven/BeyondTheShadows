from .Camera import Camera
from .Enemy import Enemy
from .Helpers import iter_list_reverse
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
        enemy: Enemy
        for enemy_index, enemy in iter_list_reverse(self.enemies):
            if enemy.health <= 0:
                del self.enemies[enemy_index]

            enemy.update(player, map_, potion_handler)
            enemy.move(map_)
            enemy.draw(camera)
