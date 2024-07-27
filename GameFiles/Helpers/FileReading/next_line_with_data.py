from typing import TextIO


def next_line_with_data(file: TextIO) -> str:
    """
    Finds the next line containing data in the given file.
    Empty lines are ignored.
    Lines starting with '#' are ignored.
    """

    for line in file:
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue

        return line
