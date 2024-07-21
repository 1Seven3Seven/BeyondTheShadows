import pathlib

import pygame

import GameFiles


class Game:
    def __init__(self, window: pygame.Surface | None = None):
        self.window: pygame.Surface = window
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.running = True
        """Is True whilst the game is running."""

        self.player: GameFiles.Player = GameFiles.Player()

        self.enemies = [
            GameFiles.BasicEnemy(200, 200)
        ]

        self.map: GameFiles.Map = GameFiles.Map(
            GameFiles.MapData.from_file(pathlib.Path("GameFiles/Maps/test.mapdata")))

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

        self.player.move(keys, self.map)

        for tile_rect in self.map.tiles.values():
            pygame.draw.rect(self.window, (255, 127, 127), tile_rect)

        for enemy in self.enemies:
            enemy.update(self.player)
            enemy.move(self.map)

            enemy.draw(self.window)

        self.player.draw(self.window)
        pygame.display.flip()

        tick = self.clock.tick(60)
        # print(tick)


def main():
    pygame.init()
    pygame.display.set_caption("Beyond The Shadows")
    window = pygame.display.set_mode((1280, 720))

    game = Game(window)

    while game.running:
        game.step()


if __name__ == "__main__":
    main()
