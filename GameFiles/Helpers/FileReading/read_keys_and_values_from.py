import pathlib

from .lines_with_data import lines_with_data
from .next_line_with_data import next_line_with_data


def read_keys_and_values_from(file: pathlib.Path) -> dict[str, list[str]]:
    """
    Reads the keys and values from a file.
    Lines that start with a : are considered keys (sans colon).
    Everything till the next key or the end of the file is considered the value.
    The values are seperated by line and stripped of preceding and trailing whitespace.
    """

    data: dict[str, list[str]] = {}

    with file.open() as f:
        line = next_line_with_data(f)

        if not line.startswith(":"):
            raise ValueError("No key was found before data")

        key: str = line[1:]
        values: list[str] = []

        if not key:
            raise ValueError("First line with key is empty")

        for line in lines_with_data(f):
            # If we have found a new key
            if line.startswith(":"):
                # Save the old key
                data[key] = values

                # Reset
                key = line[1:]
                values = []

                # Make sure the key is not empty
                if not key:
                    raise ValueError("Empty key found")

                continue

            # If we have found data
            values.append(line)

        # Do not forget the last key
        data[key] = values

    return data
