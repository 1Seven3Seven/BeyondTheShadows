import pygame

_Coords = tuple[int | float, int | float]


class Camera:
    def __init__(self, window: pygame.Surface):
        self.window = window

        self.rect = self.window.get_rect()

    def center_on(self, rect: pygame.Rect):
        self.rect.center = rect.center

    def coordinates_to_display_coordinates(self, coords: _Coords) -> _Coords:
        """
        Converts coordinates in the world to coordinates in the camera.
        """

        return coords[0] - self.rect.x, coords[1] - self.rect.y

    def convert_rect_to_camera_coordinates(self, rect: pygame.Rect) -> None:
        """
        Moves the top left of the rectangle to be in camera coordinates.
        """

        rect.topleft = self.coordinates_to_display_coordinates(rect.topleft)

    def can_see(self, rect: pygame.Rect) -> bool:
        """
        Returns true if the camera can see the given rectangle.
        Assumes that the rectangle is in camera coordinates.
        """

        return self.rect.colliderect(rect)
