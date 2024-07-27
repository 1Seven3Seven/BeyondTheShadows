from typing import TextIO, Generator

from .next_line_with_data import next_line_with_data


def lines_with_data(file: TextIO) -> Generator[str, None, None]:
    """
    Iterates through a file and yields each line of the file that contains data.
    Uses `next_line_with_data` to read the data from the file.
    """

    while True:
        line = next_line_with_data(file)

        if line is None:
            return

        yield line
