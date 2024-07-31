from typing import Literal

from .Camera import Camera
from .Helpers import iter_list_reverse
from .Map import Map
from .MapData import MapData
from .ParticleHandler import ParticleHandler
from .Player import Player
from .UpgradeBase import UpgradeBase
from .UpgradeDirectDamage import UpgradeDirectDamage
from .UpgradeExplodedPotionLifespan import UpgradeExplodedPotionLifespan
from .UpgradeLightRadius import UpgradeLightRadius
from .UpgradeThrowVelocity import UpgradeThrowVelocity

_UPGRADE_KEYS = Literal[
    "u_direct_damage",
    "u_exploded_potion_lifespan",
    "u_light_radius",
    "u_throw_velocity"
]

_UPGRADE_KEY_TO_CLASS: dict[_UPGRADE_KEYS, type(UpgradeBase)] = {
    "u_direct_damage": UpgradeDirectDamage,
    "u_exploded_potion_lifespan": UpgradeExplodedPotionLifespan,
    "u_light_radius": UpgradeLightRadius,
    "u_throw_velocity": UpgradeThrowVelocity
}


class UpgradeHandler:
    def __init__(self):
        self.upgrades: list[UpgradeBase] = []

    def setup_upgrades_from(self, map_data: MapData, map_: Map) -> None:
        """
        Clears the current upgrades list and create new upgrades from the map data.
        """

        self.upgrades = []

        for upgrade_key, tile_key, tile_offset in map_data.upgrades:
            if upgrade_key not in _UPGRADE_KEY_TO_CLASS:
                raise ValueError(f"Unknown upgrade key '{upgrade_key}'")

            new_upgrade: UpgradeBase
            new_upgrade = _UPGRADE_KEY_TO_CLASS[upgrade_key](  # NOQA: upgrade key is a str, not a literal as above
                tile_key[0] * map_.TILE_SIZE + map_.TILE_SIZE_2 + tile_offset[0],
                tile_key[1] * map_.TILE_SIZE + map_.TILE_SIZE_2 + tile_offset[1]
            )

            self.upgrades.append(new_upgrade)

    def update_and_draw_upgrades(self, player: Player, particle_handler: ParticleHandler, camera: Camera) -> None:
        upgrade: UpgradeBase
        for upgrade_index, upgrade in iter_list_reverse(self.upgrades):
            upgrade.update(player, particle_handler)
            upgrade.draw(camera)

            if upgrade.used:
                del self.upgrades[upgrade_index]
