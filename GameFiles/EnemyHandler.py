from typing import Literal

from .Camera import Camera
from .Enemy import Enemy
from .EnemyConsumer import EnemyConsumer
from .EnemyDarkling import EnemyDarkling
from .EnemyStalker import EnemyStalker
from .Helpers import iter_list_reverse
from .Map import Map
from .MapData import MapData
from .Player import Player
from .PotionHandler import PotionHandler

_ENEMY_KEYS = Literal["stalker", "consumer", "darkling"]

_ENEMY_KEY_TO_CLASS: dict[_ENEMY_KEYS, type(Enemy)] = {
    "stalker": EnemyStalker,
    "consumer": EnemyConsumer,
    "darkling": EnemyDarkling
}


class EnemyHandler:
    def __init__(self):
        self.enemies: list[Enemy] = []

    def setup_enemies_from(self, map_data: MapData, map_: Map) -> None:
        """
        Clears the current enemies list and creates new enemies from the map data.
        The given map should be generated from the given map data.
        """

        self.enemies = []

        for enemy_key, spawn_tile_key, room_id in map_data.enemies:
            if enemy_key not in _ENEMY_KEY_TO_CLASS:
                raise ValueError(f"Unknown enemy key '{enemy_key}'")

            new_enemy: Enemy
            new_enemy = _ENEMY_KEY_TO_CLASS[enemy_key](0, 0, update_offset=0)

            new_enemy.set_center((map_.TILE_SIZE * spawn_tile_key[0] + map_.TILE_SIZE_2,
                                  map_.TILE_SIZE * spawn_tile_key[1] + map_.TILE_SIZE_2))
            new_enemy.set_room_id(room_id if room_id is not None else -1, map_)

            self.enemies.append(new_enemy)

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
