import pathlib
from typing import Generator

from .Helpers.CommonTypes import IntCoordinates
from .Helpers.FileReading import read_keys_and_values_from

_GeneralMapData = dict[str, list[str]]
_RoomData = tuple[IntCoordinates, IntCoordinates]
_EnemyData = tuple[str, IntCoordinates, int | None]
_UpgradeData = tuple[str, IntCoordinates, IntCoordinates]


class MapData:
    def __init__(self, width: int, height: int):
        """
        Create an empty map data object.

        :param width: The width of the map.
        :param height: The height of the map.
        """

        self.width: int = width
        self.height: int = height

        self.tiles: list[list[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]
        """A 2D array representing walls in the map."""

        self.rooms: list[_RoomData] = []
        """
        Rooms are considered as rectangles inside the map, all empty tiles in the rectangle make the room.
        Rooms can overlap.
        """

        self.player_spawn: IntCoordinates | None = None
        """The tile that the player should spawn in."""

        self.enemies: list[_EnemyData] = []
        """
        Enemies are represented as their key, the tile they are to spawn in, and the room they are constrained to.
        If the room is None, then there is no constraint.
        """

        self.upgrades: list[_UpgradeData] = []
        """
        Upgrades are represented as their key, the tile they are to spawn in, and additional pixel movements.
        """

    def __str__(self, pretty: bool = False) -> str:
        tile_wall = "1"
        tile_air = "0"

        if pretty:
            tile_wall = "▉"
            tile_air = " "

        string = f"MapData({self.width}, {self.height})\n"

        for i in range(self.height):
            string += "".join([tile_wall if tile else tile_air for tile in self.tiles[i]])
            string += "\n"

        # Remove the unneeded trailing newline
        return string[:-1]

    def rows(self) -> Generator[list[int], None, None]:
        """Iterate over the rows of the map data."""

        for y in range(self.height):
            yield self.tiles[y]

    @staticmethod
    def _process_width_and_height(map_data_keys_and_values: _GeneralMapData) -> tuple[int, int]:
        if "DIMENSIONS" not in map_data_keys_and_values:
            raise ValueError(f"Could not find key 'DIMENSIONS' in map data")

        data = map_data_keys_and_values["DIMENSIONS"]
        if not data:
            raise ValueError("Found no data for key 'DIMENSIONS'")

        if len(data) != 1:
            raise ValueError(f"Expected one line of data for key 'DIMENSIONS' but found {len(data)}")
        data = data[0]

        try:
            width, height = data.split(",")
        except ValueError:
            raise ValueError(f"Expected dimensions formatted as 'WIDTH,HEIGHT' but got '{data}'")

        try:
            width = int(width)
            height = int(height)
        except ValueError:
            raise ValueError(f"Width and Height are not integers but {width}, {height}")

        return width, height

    @staticmethod
    def _process_tile_data_into(map_data_keys_and_values: _GeneralMapData, empty_map_data: "MapData") -> None:
        if "TILE_DATA" not in map_data_keys_and_values:
            raise ValueError("Could not find key 'TILE_DATA' in map data")

        data = map_data_keys_and_values["TILE_DATA"]
        if len(data) != empty_map_data.height:
            raise ValueError(f"Tile Data height {len(data)} does not match expected height {empty_map_data.height}.")

        for row_index, row in enumerate(data):
            if len(row) != empty_map_data.width:
                raise ValueError(f"Tile Data width {len(row)} does not match expected width {empty_map_data.width}.")

            for column_index in range(empty_map_data.width):
                empty_map_data.tiles[row_index][column_index] = int(row[column_index])

    @staticmethod
    def _process_player_spawn_into(map_data_keys_and_values: _GeneralMapData, empty_map_data: "MapData") -> None:
        if empty_map_data.player_spawn is not None:
            raise ValueError("When processing player spawn, given map data object already contains player spawn data")

        if "PLAYER_SPAWN" not in map_data_keys_and_values:
            raise ValueError("Could not find key 'PLAYER_SPAWN' in map data")

        data = map_data_keys_and_values["PLAYER_SPAWN"]
        if len(data) != 1:
            raise ValueError(f"Expected one line of data for key 'PLAYER_SPAWN' but found {len(data)}")
        data = data[0]

        try:
            tile_x, tile_y = data.split(",")
        except ValueError:
            raise ValueError(f"Expected player spawn formatted as 'TILE_X,TILE_Y' but got '{data}'")

        try:
            tile_x = int(tile_x)
            tile_y = int(tile_y)
        except ValueError:
            raise ValueError(f"Error when attempting to convert player spawn tile x and y into integers")

        empty_map_data.player_spawn = tile_x, tile_y

    @staticmethod
    def _process_room(room_str: str) -> _RoomData:
        try:
            x1, y1, x2, y2 = map(int, room_str.split(","))
        except ValueError:
            raise ValueError(f"Could not parse room string '{room_str}', expected as 'X1,Y1,X2,Y2'")

        return (x1, y1), (x2, y2)

    @staticmethod
    def _process_rooms_into(map_data_keys_and_values: _GeneralMapData, empty_map_data: "MapData") -> None:
        if empty_map_data.rooms:
            raise ValueError(f"When asked to process rooms, given map data object already contains rooms")

        # Rooms are completely optional
        if "ROOMS" not in map_data_keys_and_values:
            return

        data = map_data_keys_and_values["ROOMS"]
        if not data:
            # If the key is found, I assume you want rooms, but there is no data
            raise ValueError("Found no data for key 'ROOMS'")

        for room_str in data:
            empty_map_data.rooms.append(MapData._process_room(room_str))

    @staticmethod
    def _process_enemy(enemy_str: str) -> _EnemyData:
        try:
            enemy_key, tile_x, tile_y, room_id = enemy_str.split(",")
        except ValueError:
            raise ValueError("Error unpacking enemy string")

        try:
            tile_x = int(tile_x)
            tile_y = int(tile_y)
        except ValueError:
            raise ValueError(f"Could not parse enemy string '{enemy_str}' due to invalid tile coordinates")

        if room_id:
            try:
                room_id = int(room_id)
            except ValueError:
                raise ValueError(f"Could not parse enemy string '{enemy_str}' due to invalid room id")
        else:
            room_id = None

        return enemy_key, (tile_x, tile_y), room_id

    @staticmethod
    def _process_enemies_into(map_data_keys_and_values: _GeneralMapData, empty_map_data: "MapData") -> None:
        if empty_map_data.enemies:
            raise ValueError(f"When asked to process enemies, given map data object already contains enemies")

        # Enemies are completely optional
        if "ENEMIES" not in map_data_keys_and_values:
            return

        data = map_data_keys_and_values["ENEMIES"]
        if not data:
            raise ValueError("Found no data for key 'ENEMIES'")

        for enemy_str in data:
            empty_map_data.enemies.append(MapData._process_enemy(enemy_str))

    @staticmethod
    def _process_upgrade(upgrade_str: str) -> _UpgradeData:
        try:
            upgrade_key, tile_x, tile_y, tile_offset_x, tile_offset_y = upgrade_str.split(",")
        except ValueError:
            raise ValueError("Error unpacking upgrade string")

        try:
            tile_x = int(tile_x)
            tile_y = int(tile_y)
        except ValueError:
            raise ValueError(f"Could not parse upgrade string '{upgrade_key}' due to invalid tile coordinates")

        try:
            tile_offset_x = int(tile_offset_x)
            tile_offset_y = int(tile_offset_y)
        except ValueError:
            raise ValueError(f"Could not parse upgrade string '{upgrade_key}' due to invalid tile offsets")

        return upgrade_key, (tile_x, tile_y), (tile_offset_x, tile_offset_y)

    @staticmethod
    def _process_upgrades_into(map_data_keys_and_values: _GeneralMapData, empty_map_data: "MapData") -> None:
        if empty_map_data.upgrades:
            raise ValueError(f"When asked to process upgrades, given map data object already contains upgrades")

        # Upgrades are completely optional
        if "UPGRADES" not in map_data_keys_and_values:
            return

        data = map_data_keys_and_values["UPGRADES"]
        if not data:
            raise ValueError("Found no data for key 'UPGRADES'")

        for upgrade_str in data:
            empty_map_data.upgrades.append(MapData._process_upgrade(upgrade_str))

    @staticmethod
    def from_file(path: pathlib.Path) -> "MapData":
        """
        Creates a MapData object from a .mapdata file.

        :param path: The path to the map data file.
        """

        if not path.is_file():
            raise FileNotFoundError(f"File {path} does not exist.")

        if not path.suffix == ".mapdata":
            raise ValueError("File must be an .mapdata file.")

        map_data_keys_and_values = read_keys_and_values_from(path)

        map_data = MapData(*MapData._process_width_and_height(map_data_keys_and_values))
        MapData._process_tile_data_into(map_data_keys_and_values, map_data)
        MapData._process_player_spawn_into(map_data_keys_and_values, map_data)
        MapData._process_rooms_into(map_data_keys_and_values, map_data)
        MapData._process_enemies_into(map_data_keys_and_values, map_data)
        MapData._process_upgrades_into(map_data_keys_and_values, map_data)

        return map_data


def main():
    map_data = MapData.from_file(pathlib.Path("Maps/demo.mapdata"))

    print(map_data)
    print()
    print(map_data.__str__(pretty=True))


if __name__ == "__main__":
    main()
