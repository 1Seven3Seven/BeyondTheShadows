import asyncio
import sys

import pygame


def upon_exit():
    """
Function to be called upon wanting the pygame screen to close.
    """

    pygame.display.quit()
    sys.exit("Pygame screen close")


pygame.init()
pygame.display.set_caption("Title")
window_size = (1280, 720)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()


async def main():
    rect = pygame.rect.Rect([100, 100, 100, 100])

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                upon_exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    upon_exit()

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            rect.y -= 5
        if keys[pygame.K_DOWN]:
            rect.y += 5
        if keys[pygame.K_LEFT]:
            rect.x -= 5
        if keys[pygame.K_RIGHT]:
            rect.x += 5

        pygame.draw.rect(screen, (255, 255, 255), rect)

        """BELOW"""
        """ABOVE"""

        pygame.display.flip()

        await asyncio.sleep(0)
        # clock.tick(60)


asyncio.run(main())
