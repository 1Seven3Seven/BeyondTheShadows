import pathlib

import pygame

import GameFiles


class Game:
    def __init__(self, window: pygame.Surface):
        self.window: pygame.Surface = window
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.running = True
        """Is True whilst the game is running."""

        self.window_closed: bool = False
        """Set to True if the user attempted to close the game window."""

        self.camera: GameFiles.Camera = GameFiles.Camera(self.window)
        self.camera.rect.height -= 100  # Accommodating the ui

        self.particle_handler: GameFiles.ParticleHandler = GameFiles.ParticleHandler()
        self.particle_handler.add_particle_directory(pathlib.Path("GameFiles/Particles"))

        self.map_data: GameFiles.MapData | None = None
        self.map: GameFiles.Map = GameFiles.Map()
        self.shadows: GameFiles.Shadows = GameFiles.Shadows()
        self.potion_handler: GameFiles.PotionHandler = GameFiles.PotionHandler()
        self.player: GameFiles.Player = GameFiles.Player()
        self.upgrade_handler: GameFiles.UpgradeHandler = GameFiles.UpgradeHandler()
        self.enemy_handler: GameFiles.EnemyHandler = GameFiles.EnemyHandler()
        self.user_interface: GameFiles.UserInterface = GameFiles.UserInterface()

        self.generate_from_map_data(pathlib.Path("GameFiles/Maps/test.mapdata"))

    def generate_from_map_data(self, map_data_file: pathlib.Path) -> None:
        """
        Generates everything from the map data file.
        """

        self.map_data = GameFiles.MapData.from_file(map_data_file)

        self.regenerate_with_stored_map_data()

    def regenerate_with_stored_map_data(self) -> None:
        """
        Regenerates everything from the stored map data object.
        """

        if self.map_data is None:
            raise ValueError("No internal map data object to regenerate from.")

        self.running = True

        self.map.generate_from(self.map_data)

        self.camera.set_min_max_position(*self.map.min_max_positions())

        self.shadows.setup_for_map(self.map)

        self.potion_handler.clear_potions()

        self.player.setup_from(self.map_data, self.map)

        self.upgrade_handler.setup_upgrades_from(self.map_data, self.map)

        self.enemy_handler.setup_enemies_from(self.map_data, self.map)

        self.user_interface.setup_from(self.map_data, self.upgrade_handler, self.enemy_handler, self.window)

    def step(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.window_closed = True
                return

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self.running = False
            #         return

        if self.player.death_animation_finished:
            self.running = False
            return

        self.window.fill((127, 127, 127))

        keys = pygame.key.get_pressed()
        mouse_state = GameFiles.Helpers.get_mouse_state()

        self.potion_handler.update(self.map, self.enemy_handler.enemies, self.shadows, self.particle_handler)

        self.player.move(keys, self.map)
        self.player.update(keys, mouse_state, self.potion_handler, self.shadows)

        self.camera.center_on(self.player.rect)

        self.player.draw(self.camera)
        self.potion_handler.draw(self.camera)
        self.map.draw(self.camera)

        self.upgrade_handler.update_and_draw_upgrades(self.player, self.camera)

        self.enemy_handler.update_move_and_draw_enemies(self.player, self.map, self.potion_handler, self.camera)

        self.particle_handler.update_and_draw_particles(self.camera)

        self.shadows.update()
        self.shadows.render(self.camera)

        self.user_interface.update(self.player, self.upgrade_handler, self.enemy_handler)
        self.user_interface.render(self.window)

        pygame.display.flip()

        self.clock.tick(60)


def main():
    pygame.init()
    pygame.display.set_caption("Beyond The Shadows")
    window = pygame.display.set_mode((1280, 720))

    game = Game(window)

    while not game.window_closed:
        while game.running:
            game.step()

        game.regenerate_with_stored_map_data()


if __name__ == "__main__":
    main()
