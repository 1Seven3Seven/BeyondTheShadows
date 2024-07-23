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

    def surrounding_tiles(self, x: int, y: int) -> list[pygame.Rect]:
        """
        Given a position, return all tiles that exist surrounding it.
        """

        tile_x_base = x // self.TILE_SIZE
        tile_y_base = y // self.TILE_SIZE

        rectangles = []
        for x_diff in range(-1, 2):
            tile_x = tile_x_base + x_diff

            if tile_x < 0:
                continue
            if tile_x >= self.width:
                continue

            for y_diff in range(-1, 2):
                tile_y = tile_y_base + y_diff

                if tile_y < 0:
                    continue
                if tile_y >= self.height:
                    continue

                tile_str = f"{tile_x},{tile_y}"

                if tile_str in self.tiles:
                    rectangles.append(self.tiles[tile_str])

        return rectangles
