import math
from typing import Generator

import pygame

from .Camera import Camera
from .LightSource import LightSource


class ShadowTile:
    def __init__(self):
        self.darkness: int = 255
        """
        255 = full darkness
        """

        self.affecting_light_sources: dict[LightSource, int] = {}
        """
        A dictionary of affecting light source to the effect on the darkness.
        The effect is the reduction of the darkness of this tile.
        
        self.affecting_light_sources[some_light_source] = some_int {0 < some_int <= 255}
        """

    def calculate_darkness(self) -> None:
        """
        Calculate the darkness given the light sources that affect this tile.
        """

        if self.affecting_light_sources:
            self.darkness = 255 - max(self.affecting_light_sources.values())
        else:
            self.darkness = 255

        if self.darkness < 0:
            self.darkness = 0

    def add_light_source(self, light_source: LightSource, distance: float) -> None:
        """
        Adds the light source to the internal dictionary of affecting light sources.
        """

        multiplier = 1 - distance / light_source.radius * 0.5

        self.affecting_light_sources[light_source] = int(light_source.brightness * multiplier)
        self.calculate_darkness()

    def remove_light_source(self, light_source: LightSource) -> None:
        """
        Removes the light source from the internal dictionary of affecting light sources.
        """

        if light_source in self.affecting_light_sources:
            del self.affecting_light_sources[light_source]
            self.calculate_darkness()


class Shadows:
    TILE_SIZE = 16
    """The size of the tiles for the simulated shadows."""

    TILE_SIZE_2 = TILE_SIZE / 2
    """Half the tile size."""

    def __init__(self, width: int, height: int):
        """
        :param width: The width in number of tiles.
        :param height: The height in number of tiles.
        """

        self.tiles: list[list[ShadowTile]] = [
            [
                ShadowTile() for _ in range(width)
            ] for _ in range(height)
        ]

        self.width: int = width
        self.height: int = height

        self.light_sources: list[LightSource] = []

    def _tiles_affected_by(self, light_source: LightSource) -> Generator[tuple[ShadowTile, float], None, None]:
        """
        Iterates over all tiles that are affected by the light source.
        Each iterations returns an affected tile and the distance to that tile squared.
        """

        # Convert the position into a tile
        base_tile_x = int(light_source.x // self.TILE_SIZE)
        base_tile_y = int(light_source.y // self.TILE_SIZE)

        # Convert the radius into tile sizes
        light_radius_tiles = int(light_source.radius // self.TILE_SIZE) + 1

        # Square the light radius
        light_radius_squared = light_source.radius * light_source.radius

        # Loop over the tiles and yield if they touch the light source
        for x_diff in range(-light_radius_tiles, light_radius_tiles + 1):
            tile_x = base_tile_x + x_diff

            if tile_x < 0 or tile_x >= self.width:
                continue

            x_distance_tile = tile_x * self.TILE_SIZE + self.TILE_SIZE_2 \
                              - light_source.x  # NOQA - PEP 8: E127 continuation line over-indented for visual indent

            for y_diff in range(-light_radius_tiles, light_radius_tiles + 1):
                tile_y = base_tile_y + y_diff

                if tile_y < 0 or tile_y >= self.height:
                    continue

                y_distance_tile = tile_y * self.TILE_SIZE + self.TILE_SIZE_2 \
                                  - light_source.y  # NOQA - PEP 8: E127 continuation line over-indented for visual indent

                # Get the distance to the tile
                distance_to_tile_squared = x_distance_tile * x_distance_tile + y_distance_tile * y_distance_tile

                # If close enough yield
                if distance_to_tile_squared <= light_radius_squared:
                    yield self.tiles[tile_y][tile_x], distance_to_tile_squared

    def add_light_source(self, light_source: LightSource) -> None:
        # Add the light source
        self.light_sources.append(light_source)

        # Update any affected tiles
        for affected_tile, distance_squared in self._tiles_affected_by(light_source):
            affected_tile.add_light_source(light_source, math.sqrt(distance_squared))

    def remove_light_source(self, light_source: LightSource) -> None:
        # Skip if not present
        if light_source not in self.light_sources:
            return

        # Bye
        self.light_sources.remove(light_source)

        # Update any affected tiles
        for affected_tile, _ in self._tiles_affected_by(light_source):
            affected_tile.remove_light_source(light_source)

    def render(self, camera: Camera) -> None:
        tile_surface = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        tile_rect = tile_surface.get_rect()

        for tile_x in range(self.width):
            tile_x_position = tile_x * self.TILE_SIZE

            for tile_y in range(self.height):
                tile_y_position = tile_y * self.TILE_SIZE

                tile_rect.topleft = tile_x_position, tile_y_position

                if not camera.can_see(tile_rect):
                    continue

                camera.convert_rect_to_camera_coordinates(tile_rect)

                tile_darkness = self.tiles[tile_y][tile_x].darkness
                tile_surface.fill((tile_darkness, tile_darkness, tile_darkness))

                camera.window.blit(tile_surface, tile_rect, special_flags=pygame.BLEND_RGB_SUB)
