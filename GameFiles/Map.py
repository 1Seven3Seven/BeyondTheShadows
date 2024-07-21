import pygame

from .MapData import MapData

TILE_SIZE = 128


class Map:
    def __init__(self, map_data: MapData | None = None):
        self.tiles: dict[str, pygame.Rect] = {}
        """
        A string of tile coords "x,y" to collision rectangle.
        """

        self.width: int = 0
        self.height: int = 0

        if map_data is not None:
            self.generate_from(map_data)

    def generate_from(self, map_data: MapData):
        self.tiles = {}

        for y, row in enumerate(map_data.rows()):
            for x, tile in enumerate(row):
                if tile == 0:
                    continue

                self.tiles[f"{x},{y}"] = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        self.width = map_data.width
        self.height = map_data.height
