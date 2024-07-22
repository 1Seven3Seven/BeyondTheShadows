class LightSource:
    def __init__(self, x: int | float, y: int | float, brightness: int, radius: int):
        """
        :param x: The x coordinate of the light source.
        :param y: The y coordinate of the light source.
        :param brightness: The brightness at the center of the light source.
        :param radius: The radius of the light source.
        """

        self.x = x
        self.y = y

        self.brightness = brightness
        self.radius = radius
