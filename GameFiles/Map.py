import pygame

from .Camera import Camera
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

        self.x_min: int = 0
        """The minimum x coordinate that exists within the map tiles."""
        self.x_max: int = 0
        """The maximum x coordinate that exists within the map tiles."""
        self.y_min: int = 0
        """The minimum y coordinate that exists within the map tiles."""
        self.y_max: int = 0
        """The maximum y coordinate that exists within the map tiles."""

        if map_data is not None:
            self.generate_from(map_data)

    def min_max_positions(self) -> tuple[int, int, int, int]:
        """
        Returns the min and max coordinates of the map tiles.

        :return: the min and max coordinates of the map tiles as (x_min, x_max, y_min, y_max)
        """

        return self.x_min, self.x_max, self.y_min, self.y_max

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

        self.x_min = 0
        self.x_max = self.TILE_SIZE * self.width
        self.y_min = 0
        self.y_max = self.TILE_SIZE * self.height

    def surrounding_tiles(self, x: int, y: int) -> list[pygame.Rect]:
        """
        Given a position, return all tiles that exist surrounding it.
        """

        tile_x_base = int(x // self.TILE_SIZE)
        tile_y_base = int(y // self.TILE_SIZE)

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

    def draw(self, camera: Camera):
        for tile_rect in self.tiles.values():
            if not camera.can_see(tile_rect):
                continue

            display_rect = tile_rect.copy()
            camera.convert_rect_to_camera_coordinates(display_rect)

            pygame.draw.rect(camera.window, (255, 127, 127), display_rect)
