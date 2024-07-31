import pygame

from . import UpgradeDirectDamage, UpgradeExplodedPotionLifespan, UpgradeLightRadius, UpgradeThrowVelocity
from .EnemyHandler import EnemyHandler
from .MapData import MapData
from .Player import Player
from .UpgradeHandler import UpgradeHandler

_Colour = tuple[int, int, int]


class UserInterface:
    UI_BOARDER_HEIGHT: int = 100
    UI_BOARDER_COLOUR: _Colour = (70, 70, 70)

    UI_BASE_COLOUR: _Colour = (140, 140, 140)

    PLAYER_HEALTH_RECT_WIDTH: int = 600
    PLAYER_HEALTH_RECT_COLOUR: _Colour = (255, 0, 0)
    PLAYER_HEALTH_RECT_BOARDER_COLOUR: _Colour = (150, 0, 0)

    PLAYER_DAMAGE_RECT_COLOUR: _Colour = (50, 50, 50)
    PLAYER_DAMAGE_RECT_BOARDER_COLOUR: _Colour = (0, 0, 0)

    def __init__(self):
        self.font: pygame.font.Font = pygame.font.SysFont(None, 32)

        self.window_size: tuple[int, int] = 0, 0

        self.ui_boarder: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.ui_base: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self.player_health_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.player_damage_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self.potion_sprite: pygame.Surface = pygame.Surface((50, 50))
        pygame.draw.circle(self.potion_sprite, (0, 255, 0), (25, 25), 25)
        # ToDo: load potion sprite
        self.potion_cover_surface: pygame.Surface = pygame.Surface(self.potion_sprite.get_size())
        self.potion_surface: pygame.Surface = pygame.Surface(self.potion_sprite.get_size(), flags=pygame.SRCALPHA)
        self.potion_surface.set_colorkey((0, 0, 0))
        self.potion_surface_rect: pygame.Rect = self.potion_surface.get_rect()

        self.enemy_count: int = 0
        self.upgrade_count: int = 0

        self.enemy_text_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.upgrade_text_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

        self.recent_upgrade_text: str = ""
        self.recent_upgrade_text_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    def _setup_potion_sprite(self) -> None:
        pass

    def setup_from(self, map_data: MapData, upgrade_handler: UpgradeHandler, enemy_handler: EnemyHandler,
                   window: pygame.Surface) -> None:
        """
        Expects the upgrade handler and enemy handler to be already set up from the same map data.
        """

        self.window_size = window.get_size()

        self.ui_boarder.update(0, 720 - self.UI_BOARDER_HEIGHT, 1280, self.UI_BOARDER_HEIGHT)
        self.ui_base.update(self.ui_boarder.x + 10, self.ui_boarder.y + 10,
                            self.ui_boarder.width - 20, self.ui_boarder.height - 20)

        self.player_health_rect.update(self.ui_base.x + 10, self.ui_base.y + 10,
                                       self.PLAYER_HEALTH_RECT_WIDTH, self.ui_base.height - 20)
        self.player_damage_rect.update(self.player_health_rect.right, self.player_health_rect.y,
                                       0, self.player_health_rect.height)

        self.enemy_count = len(enemy_handler.enemies)
        self.upgrade_count = len(upgrade_handler.upgrades)

    def _update_potion_surface(self, player: Player) -> None:
        self.potion_cover_surface.fill((0, 0, 0))
        cover_rect_height = int(self.potion_sprite.get_height() * player.attack_delay / player.ATTACK_DELAY)
        pygame.draw.rect(self.potion_cover_surface, (50, 50, 50),
                         pygame.Rect(0, 50 - cover_rect_height, 50, cover_rect_height))

        self.potion_surface.blit(self.potion_sprite, (0, 0))
        self.potion_surface.blit(self.potion_cover_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    def _update_recent_upgrade(self, upgrade_handler: UpgradeHandler) -> None:
        if upgrade_handler.most_recent_collected_upgrade is None:
            return

        if isinstance(upgrade_handler.most_recent_collected_upgrade, UpgradeDirectDamage):
            self.recent_upgrade_text = "Damage +"
        elif isinstance(upgrade_handler.most_recent_collected_upgrade, UpgradeExplodedPotionLifespan):
            self.recent_upgrade_text = "Potion time +"
        elif isinstance(upgrade_handler.most_recent_collected_upgrade, UpgradeLightRadius):
            self.recent_upgrade_text = "Light +"
        elif isinstance(upgrade_handler.most_recent_collected_upgrade, UpgradeThrowVelocity):
            self.recent_upgrade_text = "Velocity +"

    def update(self, player: Player, upgrade_handler: UpgradeHandler, enemy_handler: EnemyHandler) -> None:
        new_width = int(player.health / player.HEALTH * self.PLAYER_HEALTH_RECT_WIDTH)
        if new_width < 0:
            new_width = 0
        elif new_width == 0 and player.health > 0:
            new_width = 1

        self.player_health_rect.width = new_width
        self.player_damage_rect.width = self.PLAYER_HEALTH_RECT_WIDTH - new_width
        self.player_damage_rect.x = self.player_health_rect.right

        self._update_potion_surface(player)

        self.upgrade_count = len(upgrade_handler.upgrades)
        self.enemy_count = len(enemy_handler.enemies)

        self._update_recent_upgrade(upgrade_handler)

    def _draw_player_health_rect(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, self.PLAYER_HEALTH_RECT_COLOUR, self.player_health_rect)
        pygame.draw.rect(window, self.PLAYER_HEALTH_RECT_BOARDER_COLOUR, self.player_health_rect, 5)
        pygame.draw.rect(window, self.PLAYER_DAMAGE_RECT_COLOUR, self.player_damage_rect)
        pygame.draw.rect(window, self.PLAYER_DAMAGE_RECT_BOARDER_COLOUR, self.player_damage_rect, 5)

    def _draw_enemies_left(self, window: pygame.Surface) -> None:
        rendered_text = self.font.render(f"Enemies left: {self.enemy_count}", True, (255, 255, 255))
        self.enemy_text_rect = rendered_text.get_rect()

        self.enemy_text_rect.centery = self.player_damage_rect.centery
        self.enemy_text_rect.x = self.player_damage_rect.right + 10 + self.potion_surface.get_width() + 30

        window.blit(rendered_text, self.enemy_text_rect)

    def _draw_upgrades_left(self, window: pygame.Surface) -> None:
        rendered_text = self.font.render(f"Upgrades left: {self.upgrade_count}", True, (255, 255, 255))
        self.upgrade_text_rect = rendered_text.get_rect()

        self.upgrade_text_rect.centery = self.player_damage_rect.centery
        self.upgrade_text_rect.x = self.enemy_text_rect.right + 30

        window.blit(rendered_text, self.upgrade_text_rect)

    def _draw_most_recent_upgrade(self, window: pygame.Surface) -> None:
        rendered_text: pygame.Surface = self.font.render(self.recent_upgrade_text, True, (255, 255, 255))
        self.recent_upgrade_text_rect = rendered_text.get_rect()

        self.recent_upgrade_text_rect.centery = self.upgrade_text_rect.centery
        self.recent_upgrade_text_rect.x = self.upgrade_text_rect.right + 30

        window.blit(rendered_text, self.recent_upgrade_text_rect)

    def render(self, window: pygame.Surface) -> None:
        # Draw the base of the ui
        pygame.draw.rect(window, self.UI_BOARDER_COLOUR, self.ui_boarder)
        pygame.draw.rect(window, self.UI_BASE_COLOUR, self.ui_base)

        self._draw_player_health_rect(window)

        window.blit(self.potion_surface, (self.player_damage_rect.right + 10, self.player_damage_rect.y + 5))

        self._draw_enemies_left(window)
        self._draw_upgrades_left(window)
        self._draw_most_recent_upgrade(window)
