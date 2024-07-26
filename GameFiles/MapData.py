import pathlib
from typing import Generator, TextIO


class MapData:
    def __init__(self, width: int, height: int):
        """
        Create an empty map data object.

        :param width: The width of the map.
        :param height: The height of the map.
        """

        self.width: int = width
        self.height: int = height

        self.tiles: list[list[int]] = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

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
    def next_line_with_data(file: TextIO) -> str:
        """Get the next line containing data in the file."""

        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            return line

    @classmethod
    def lines_with_data(cls, file: TextIO) -> Generator[str, None, None]:
        """Iterate over each line of data in the file."""

        while True:
            line = cls.next_line_with_data(file)

            if line is None:
                break

            yield line

    @classmethod
    def read_map_dimensions(cls, file: TextIO) -> tuple[int, int]:
        """
        Reads the width and height of the map data from the file.

        Assumes that the file has not been read from yet.
        """

        line = cls.next_line_with_data(file)

        if line != "DIMENSIONS":
            raise ValueError(f"Expected 'DIMENSIONS' but got '{line}'")

        line = cls.next_line_with_data(file)

        try:
            width, height = line.split(",")
        except ValueError:
            raise ValueError(f"Expected 'WIDTH,HEIGHT' but got '{line}'")

        return int(width), int(height)

    @classmethod
    def read_map_tile_data_into(cls, file: TextIO, empty_map_data: "MapData") -> None:
        """
        Reads the tile data of the map from the file into the given map data object.
        Uses the width and height already in the object.
        """

        line = cls.next_line_with_data(file)

        if line != "TILE_DATA":
            raise ValueError(f"Expected 'TILE_DATA' but got '{line}'")

        row_index = 0  # Preventing pycharm from yelling at me
        for row_index in range(empty_map_data.height):
            line = cls.next_line_with_data(file)

            if len(line) != empty_map_data.width:
                raise ValueError(f"Data width {len(line)} does not match expected width {empty_map_data.width}.")

            for column_index in range(empty_map_data.width):
                empty_map_data.tiles[row_index][column_index] = int(line[column_index])

        row_index += 1

        if row_index != empty_map_data.height:
            raise ValueError(f"Data height {row_index} does not match expected height {empty_map_data.height}.")

    @classmethod
    def from_file(cls, path: pathlib.Path) -> "MapData":
        """
        Creates a MapData object from a .mapdata file.

        :param path: The path to the map data file.
        """

        if not path.is_file():
            raise FileNotFoundError(f"File {path} does not exist.")

        if not path.suffix == ".mapdata":
            raise ValueError("File must be an .mapdata file.")

        with path.open() as file:
            # Generate an empty map data object
            map_data = cls(*cls.read_map_dimensions(file))

            # Fill the map data object with, well, map data
            cls.read_map_tile_data_into(file, map_data)

            # ToDo: continue reading the file for any optional entries
            # ToDo: create the optional entries to read
            # Those should probably be the other way around, but ehh

        return map_data


def main():
    map_data = MapData.from_file(pathlib.Path("Maps/test.mapdata"))

    print(map_data)
    print()
    print(map_data.__str__(pretty=True))


if __name__ == "__main__":
    main()
