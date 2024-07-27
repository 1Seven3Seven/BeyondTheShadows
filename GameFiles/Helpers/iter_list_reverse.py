from typing import Generator, Any


def iter_list_reverse(some_list: list) -> Generator[tuple[int, Any], None, None]:
    """
    Iterate, in reverse, over the given list, returning each element alongside its index.
    """

    for i in range(len(some_list) - 1, -1, -1):
        yield i, some_list[i]
