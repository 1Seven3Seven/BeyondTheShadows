from typing import Generator

import pygame

from .Camera import Camera
from .Helpers.CommonTypes import Coordinates, Number, IntCoordinates
from .MapData import MapData

_TileKey = IntCoordinates


class Map:
    TILE_SIZE = 128
    TILE_SIZE_2 = int(TILE_SIZE // 2)

    def __init__(self, map_data: MapData | None = None):
        self.tiles: dict[_TileKey, pygame.Rect] = {}
        """
        A string of tile coords as a tuple (x, y) to collision rectangle.
        """

        self.rooms: list[list[_TileKey]] = []
        """
        A list of all rooms this map has.
        Rooms here are a list of all the empty tiles for the room.
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

    def _generate_tiles(self, map_data: MapData) -> None:
        self.tiles = {}

        for y, row in enumerate(map_data.rows()):
            for x, tile in enumerate(row):
                if tile == 0:
                    continue

                self.tiles[(x, y)] = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                                 self.TILE_SIZE, self.TILE_SIZE)

    def _generate_rooms(self, map_data: MapData) -> None:
        """
        Expects the tiles to be already generated.
        """

        self.rooms = []

        for room in map_data.rooms:
            x_min = room[0][0]
            y_min = room[0][1]
            x_max = room[1][0]
            y_max = room[1][1]

            if x_min > x_max:
                x_min, x_max = x_max, x_min
            if y_min > y_max:
                y_min, y_max = y_max, y_min

            if x_max >= map_data.width:
                x_max = map_data.width
            if y_max >= map_data.height:
                y_max = map_data.height

            room_tile_keys = []

            for tile_x in range(x_min, x_max + 1):
                for tile_y in range(y_min, y_max + 1):
                    tile_key = tile_x, tile_y

                    if tile_key not in self.tiles:
                        room_tile_keys.append(tile_key)

            self.rooms.append(room_tile_keys)

    def generate_from(self, map_data: MapData) -> None:
        self.width = map_data.width
        self.height = map_data.height

        self.x_min = 0
        self.x_max = self.TILE_SIZE * self.width
        self.y_min = 0
        self.y_max = self.TILE_SIZE * self.height

        self._generate_tiles(map_data)
        self._generate_rooms(map_data)

    def iter_surrounding_tile_keys(self, x: Number, y: Number) -> Generator[_TileKey, None, None]:
        """
        Iterates over the tile keys surrounding the given coordinates.
        Ignores any outside of the map.
        Does not check if the tile keys exist.
        """

        tile_x_base = int(x // self.TILE_SIZE)
        tile_y_base = int(y // self.TILE_SIZE)

        tile_x_min = tile_x_base - 1
        tile_x_max = tile_x_base + 2

        if tile_x_min < 0:
            tile_x_min = 0
        if tile_x_max >= self.width:
            tile_x_max = self.width

        tile_y_min = tile_y_base - 1
        tile_y_max = tile_y_base + 2

        if tile_y_min < 0:
            tile_y_min = 0
        if tile_y_max >= self.height:
            tile_y_max = self.height

        for tile_x in range(tile_x_min, tile_x_max):
            for tile_y in range(tile_y_min, tile_y_max):
                yield tile_x, tile_y

    def iter_surrounding_tile_keys_in_range(self, x: Number, y: Number, range_: int) -> Generator[_TileKey, None, None]:
        """
        Iterates over the tile keys surrounding the given coordinates within a range.
        The range is in tiles.
        Ignores any outside of the map.
        Does not check if the tile keys exist.
        """

        tile_x_base = int(x // self.TILE_SIZE)
        tile_y_base = int(y // self.TILE_SIZE)

        tile_x_min = tile_x_base - range_
        tile_x_max = tile_x_base + range_ + 1

        if tile_x_min < 0:
            tile_x_min = 0
        if tile_x_max >= self.width:
            tile_x_max = self.width

        tile_y_min = tile_y_base - range_
        tile_y_max = tile_y_base + range_ + 1

        if tile_y_min < 0:
            tile_y_min = 0
        if tile_y_max >= self.height:
            tile_y_max = self.height

        for tile_x in range(tile_x_min, tile_x_max):
            for tile_y in range(tile_y_min, tile_y_max):
                yield tile_x, tile_y

    def surrounding_tile_keys(self, x: Number, y: Number) -> list[_TileKey]:
        """
        Given a position, return all the keys for tiles that exist surrounding it.
        """

        tile_keys = []
        for tile_key in self.iter_surrounding_tile_keys(x, y):
            if tile_key in self.tiles:
                tile_keys.append(tile_key)

        return tile_keys

    def surrounding_empty_tile_keys(self, x: Number, y: Number) -> list[_TileKey]:
        """
        Given a position, return all the keys for tiles that do not exist surrounding it.
        """

        tile_keys = []
        for tile_key in self.iter_surrounding_tile_keys(x, y):
            if tile_key not in self.tiles:
                tile_keys.append(tile_key)
        return tile_keys

    def surrounding_tiles(self, x: Number, y: Number) -> list[pygame.Rect]:
        """
        Given a position, return all tiles that exist surrounding it.
        """

        tile_rectangles = []
        for tile_key in self.iter_surrounding_tile_keys(x, y):
            if tile_key in self.tiles:
                tile_rectangles.append(self.tiles[tile_key])

        return tile_rectangles

    def tiles_touching(self, rect: pygame.Rect) -> list[pygame.Rect]:
        """
        Given a rectangle, return all tiles that exist touching it.

        Might not work properly if the right or bottom is a negative number.
        """

        tile_x_min = int(rect.left // self.TILE_SIZE)
        tile_x_max = int(rect.right // self.TILE_SIZE) + 1

        if tile_x_min < 0:
            tile_x_min = 0
        if tile_x_max >= self.width:
            tile_x_max = self.width

        tile_y_min = int(rect.top // self.TILE_SIZE)
        tile_y_max = int(rect.bottom // self.TILE_SIZE) + 1

        if tile_y_max >= self.height:
            tile_y_max = self.height
        if tile_y_min < 0:
            tile_y_min = 0

        rectangles = []
        for tile_x in range(tile_x_min, tile_x_max):
            for tile_y in range(tile_y_min, tile_y_max):
                tile_key = (tile_x, tile_y)

                if tile_key in self.tiles:
                    rectangles.append(self.tiles[tile_key])

        return rectangles

    def tile_key_for_position(self, position: Coordinates) -> _TileKey:
        """
        Given a position, return the key for the tile that it may exist within.
        The tile for the key is not guaranteed to exist.
        """

        return int(position[0] // self.TILE_SIZE), int(position[1] // self.TILE_SIZE)

    def position_in_tile(self, position: Coordinates) -> bool:
        """
        Return true if the given position is inside a tile.
        """

        tile_key = self.tile_key_for_position(position)

        return tile_key in self.tiles

    def tile_for_position(self, position: Coordinates) -> pygame.Rect | None:
        """
        If the position is inside a tile, return the tile, else return None.
        """

        tile_key = self.tile_key_for_position(position)

        if tile_key in self.tiles:
            return self.tiles[tile_key]
        return None

    def draw(self, camera: Camera):
        display_rect = pygame.Rect(0, 0, self.TILE_SIZE, self.TILE_SIZE)

        for tile_rect in self.tiles.values():
            if not camera.can_see(tile_rect):
                continue

            display_rect.topleft = tile_rect.topleft
            camera.convert_rect_to_camera_coordinates(display_rect)

            # Used to be coloured (255, 127, 127)
            pygame.draw.rect(camera.window, (64, 64, 96), display_rect)
