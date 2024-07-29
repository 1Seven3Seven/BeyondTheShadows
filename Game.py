import pathlib

import pygame

import GameFiles


class Game:
    def __init__(self, window: pygame.Surface):
        self.window: pygame.Surface = window
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.running = True
        """Is True whilst the game is running."""

        self.map_data: GameFiles.MapData = GameFiles.MapData.from_file(pathlib.Path("GameFiles/Maps/test.mapdata"))

        self.map: GameFiles.Map = GameFiles.Map(self.map_data)

        self.shadows: GameFiles.Shadows = GameFiles.Shadows(
            self.map.width * self.map.TILE_SIZE // GameFiles.Shadows.TILE_SIZE,
            self.map.height * self.map.TILE_SIZE // GameFiles.Shadows.TILE_SIZE
        )

        self.player: GameFiles.Player = GameFiles.Player(self.shadows)

        self.potion_handler: GameFiles.PotionHandler = GameFiles.PotionHandler()

        self.particle_handler: GameFiles.ParticleHandler = GameFiles.ParticleHandler()
        self.particle_handler.add_particle_directory(pathlib.Path("GameFiles/Particles"))

        self.enemy_handler: GameFiles.EnemyHandler = GameFiles.EnemyHandler()
        self.enemy_handler.enemies.extend([
            GameFiles.BasicEnemy(200, 200),
            GameFiles.EnemyStalker(300, 300)
        ])

        self.camera: GameFiles.Camera = GameFiles.Camera(self.window)
        self.camera.set_min_max_position(*self.map.min_max_positions())

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

        self.window.fill((127, 127, 127))

        keys = pygame.key.get_pressed()
        keys_just_pressed = pygame.key.get_just_pressed()
        mouse_state = GameFiles.Helpers.get_mouse_state()

        self.potion_handler.update(self.map, self.enemy_handler.enemies, self.shadows, self.particle_handler)

        self.player.move(keys, self.map)
        self.player.update(keys, mouse_state, self.potion_handler, self.shadows)

        self.camera.center_on(self.player.rect)

        if keys_just_pressed[pygame.K_SPACE]:
            GameFiles.PotionExploded.increase_light_radius()

        self.player.draw(self.camera)
        self.map.draw(self.camera)
        self.potion_handler.draw(self.camera)

        self.enemy_handler.update_move_and_draw_enemies(self.player, self.map, self.potion_handler, self.camera)

        if keys[pygame.K_BACKSPACE]:
            if self.shadows.light_sources:
                self.shadows.remove_light_source(self.shadows.light_sources[0])

        self.particle_handler.update_and_draw_particles(self.camera)

        self.shadows.render(self.camera)

        pygame.display.flip()

        self.clock.tick(60)


def main():
    pygame.init()
    pygame.display.set_caption("Beyond The Shadows")
    window = pygame.display.set_mode((1280, 720))

    game = Game(window)

    while game.running:
        game.step()


if __name__ == "__main__":
    main()
