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
    def next_data(file: TextIO) -> str:
        """Get the next line containing data in the file."""

        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            return line

    @classmethod
    def data(cls, file: TextIO) -> Generator[str, None, None]:
        """Iterate over each line of data in the file."""

        while True:
            line = cls.next_data(file)

            if line is None:
                break

            yield line

    @classmethod
    def read_width_height(cls, file: TextIO) -> tuple[int, int]:
        """
        Reads the width and height of the map data from the file.

        Assumes that the file has not been read from yet.
        """

        line = cls.next_data(file)

        width, height = line.split(",")

        return int(width), int(height)

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
            map_data = cls(*cls.read_width_height(file))

            # Fill the map data from the file
            for i, data in enumerate(cls.data(file)):
                if len(data) != map_data.width:
                    raise ValueError(f"Data width {len(data)} does not match expected width {map_data.width}.")

                for j, tile in enumerate(data):
                    map_data.tiles[i][j] = int(tile)

        i += 1

        if i != map_data.height:
            raise ValueError(f"Data height {i} does not match expected height {map_data.height}.")

        return map_data


def main():
    map_data = MapData.from_file(pathlib.Path("Maps/test.mapdata"))

    print(map_data)
    print(map_data.__str__(pretty=True))


if __name__ == "__main__":
    main()
