import asyncio

import pygame

from Game import Game

pygame.init()
pygame.display.set_caption("Beyond The Shadows")
window = pygame.display.set_mode((1280, 720))

game = Game(window)


async def main():
    while not game.window_closed:
        while game.running:
            game.step()

            await asyncio.sleep(0)

        game.regenerate_with_stored_map_data()


asyncio.run(main())
