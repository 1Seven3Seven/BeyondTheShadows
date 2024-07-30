from .LightSource import LightSource


class ShadowTile:
    def __init__(self):
        self.darkness: int = 255
        """
        255 = full darkness
        """

        self.affecting_light_sources: dict[LightSource, int] = {}
        """
        A dictionary of affecting light source to the effect on the darkness.
        The effect is the reduction of the darkness of this tile.

        self.affecting_light_sources[some_light_source] = some_int {0 < some_int <= 255}
        """

    def calculate_darkness(self) -> None:
        """
        Calculate the darkness given the light sources that affect this tile.
        """

        if self.affecting_light_sources:
            self.darkness = 255 - max(self.affecting_light_sources.values())
        else:
            self.darkness = 255

        if self.darkness < 0:
            self.darkness = 0

    def add_light_source(self, light_source: LightSource, distance: float) -> None:
        """
        Adds the light source to the internal dictionary of affecting light sources.
        """

        multiplier = 1 - distance / light_source.radius * 0.5

        self.affecting_light_sources[light_source] = int(light_source.brightness * multiplier)
        self.calculate_darkness()

    def remove_light_source(self, light_source: LightSource) -> None:
        """
        Removes the light source from the internal dictionary of affecting light sources.
        """

        if light_source in self.affecting_light_sources:
            del self.affecting_light_sources[light_source]
            self.calculate_darkness()
