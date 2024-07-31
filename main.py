import asyncio
# import time

import pygame

from Game import Game

pygame.init()
pygame.display.set_caption("Beyond The Shadows")
window = pygame.display.set_mode((1280, 720))

game = Game(window)


async def main():
    while not game.window_closed:
        while game.running:
            # start = time.perf_counter()
            game.step()
            # time_elapsed = time.perf_counter() - start
            # time_elapsed_rounded = round(time_elapsed, 4)

            # print(f"Frame time {time_elapsed_rounded:<06}", end="")
            # if time_elapsed_rounded > 0.017:
            #     print(" - too long")
            # else:
            #     print()

            await asyncio.sleep(0)

        game.regenerate_with_stored_map_data()


asyncio.run(main())
