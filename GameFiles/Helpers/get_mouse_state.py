from typing import Literal, Any

import pygame

MouseStateKeys = Literal["position", "buttons"]
MouseSate = dict[MouseStateKeys, Any]


def get_mouse_state() -> MouseSate:
    """
    Creates and returns a dictionary representing the current state of the mouse.
    """

    return {
        "position": pygame.mouse.get_pos(),
        "buttons": pygame.mouse.get_pressed(),
    }
