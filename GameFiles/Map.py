import pygame

from .MapData import MapData


class Map:
    TILE_SIZE = 128

    def __init__(self, map_data: MapData | None = None):
        self.tiles: dict[str, pygame.Rect] = {}
        """
        A string of tile coords "x,y" to collision rectangle.
        """

        self.width: int = 0
        """The width in map tiles."""
        self.height: int = 0
        """The height in map tiles."""

        if map_data is not None:
            self.generate_from(map_data)

    def generate_from(self, map_data: MapData):
        self.tiles = {}

        for y, row in enumerate(map_data.rows()):
            for x, tile in enumerate(row):
                if tile == 0:
                    continue

                self.tiles[f"{x},{y}"] = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                                     self.TILE_SIZE, self.TILE_SIZE)

        self.width = map_data.width
        self.height = map_data.height
