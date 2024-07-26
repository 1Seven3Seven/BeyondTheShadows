import pygame

_Coords = tuple[int | float, int | float]


class Camera:
    def __init__(self, window: pygame.Surface):
        self.window = window
        """The surface to be drawn to."""

        self.rect = self.window.get_rect()
        """The cameras size and location in the world."""

        self.width_2: int = int(self.rect.width // 2)
        """Half of the window width."""
        self.height_2: int = int(self.rect.height // 2)
        """Half of the window height."""

        self.x_min: int | float = float("-inf")
        """The minimum x coordinate of the camera."""
        self.x_max: int | float = float("inf")
        """The maximum x coordinate of the camera."""
        self.y_min: int | float = float("-inf")
        """The minimum y coordinate of the camera."""
        self.y_max: int | float = float("inf")
        """The maximum y coordinate of the camera."""

    def set_min_max_position(self,
                             x_min: int | float, x_max: int | float,
                             y_min: int | float, y_max: int | float) -> None:
        """Sets the minimum and maximum coordinates of the camera."""

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def center_on(self, rect: pygame.Rect):
        self.rect.center = rect.center

        if self.rect.left < self.x_min:
            self.rect.left = self.x_min
        elif self.rect.right > self.x_max:
            self.rect.right = self.x_max

        if self.rect.top < self.y_min:
            self.rect.top = self.y_min
        elif self.rect.bottom > self.y_max:
            self.rect.bottom = self.y_max

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
