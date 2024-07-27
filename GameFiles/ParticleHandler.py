import pathlib
from typing import Any, Literal

import pygame

from .Camera import Camera
from .Helpers import iter_list_reverse
from .Helpers.FileReading import next_line_with_data
from .Particle import Particle

_ParticleDataKeys = Literal["KEY", "SIZE", "IS_SQUARE", "COLOUR"]
_ParticleEntryKeys = Literal["SPRITE"]


class ParticleHandler:
    PARTICLE_DATA: dict[str, dict[_ParticleEntryKeys, Any]] = {}
    """
    A dictionary of particle key to data for that key. 
    """

    def __init__(self):
        self.particles: list[Particle] = []

    @staticmethod
    def _read_particle_data(particle_file_path: pathlib.Path) -> dict[_ParticleDataKeys, ...]:
        particle_data = {}

        with open(particle_file_path, "r") as particle_file:
            # Read the particle key/name
            line = next_line_with_data(particle_file)
            if line != "KEY":
                raise ValueError(f"Expected 'KEY', got '{line}'")
            line = next_line_with_data(particle_file)
            particle_data["KEY"] = line

            # Read the particle shape
            line = next_line_with_data(particle_file)
            if line != "IS_SQUARE":
                raise ValueError(f"Expected 'IS_SQUARE', got '{line}'")
            line = next_line_with_data(particle_file)
            if line not in ["0", "1"]:
                raise ValueError(f"Expected either '0' or '1', got '{line}'")
            particle_data["IS_SQUARE"] = int(line)

            # Read the particle size
            line = next_line_with_data(particle_file)
            if line != "SIZE":
                raise ValueError(f"Expected 'SIZE', got '{line}'")
            line = next_line_with_data(particle_file)
            try:
                particle_data["SIZE"] = int(line)
            except ValueError:
                raise ValueError(f"Expected some integer, got '{line}'")

            # Read the particle colour
            line = next_line_with_data(particle_file)
            if line != "COLOUR":
                raise ValueError(f"Expected 'COLOUR', got '{line}'")
            line = next_line_with_data(particle_file)
            try:
                r, g, b, a = line.split(",")
                particle_data["COLOUR"] = int(r), int(g), int(b), int(a)
            except ValueError:
                raise ValueError(f"Expected line in the format 'r,g,b,a', got '{line}'")

        # Expected type 'dict[Literal["KEY", "SIZE", "IS_SQUARE", "COLOUR"], Any]',
        #  got 'dict[str, str | int | tuple[int, int, int]]' instead
        return particle_data  # NOQA: see above comment

    def _construct_particle_entry_from_data(self, particle_data: dict[_ParticleDataKeys, Any]) -> None:
        sprite_size: int
        if particle_data["IS_SQUARE"]:
            sprite_size = particle_data["SIZE"]
        else:
            sprite_size = particle_data["SIZE"] * 2

        colour = particle_data["COLOUR"]

        sprite = pygame.Surface((sprite_size, sprite_size), flags=pygame.SRCALPHA)

        if particle_data["IS_SQUARE"]:
            sprite.fill(colour)
        else:
            sprite_size_2 = int(sprite_size // 2)
            pygame.draw.circle(sprite, colour, (sprite_size_2, sprite_size_2), int(sprite_size // 2))

        key = particle_data["KEY"]

        particle_entry: dict[_ParticleEntryKeys, Any] = {
            "SPRITE": sprite
        }

        self.PARTICLE_DATA[key] = particle_entry

    def add_particle_directory(self, directory: pathlib.Path) -> None:
        if not directory.is_dir():
            raise NotADirectoryError(f"{directory} is not a directory")

        for particle_file in directory.glob("*.particle"):
            particle_data = self._read_particle_data(particle_file)

            self._construct_particle_entry_from_data(particle_data)

    def create_particle(self, particle_key: str,
                        x: int | float, y: int | float,
                        vx: int | float, vy: int | float,
                        lifespan: int) -> None:
        """
        Create a particle of type `particle_key` at the given coordinates with the given velocity.
        """

        if particle_key not in self.PARTICLE_DATA:
            raise ValueError(f"Particle key {particle_key} cannot be found in loaded particle data")

        self.particles.append(Particle(x, y, vx, vy, lifespan, self.PARTICLE_DATA[particle_key]["SPRITE"]))

    def update_particles(self) -> None:
        particle: Particle
        for particle_index, particle in iter_list_reverse(self.particles):
            if particle.lifespan <= 0:
                del self.particles[particle_index]
                continue

            particle.update()

    def draw_particles(self, camera: Camera) -> None:
        for particle in self.particles:
            particle.draw(camera)

    def update_and_draw_particles(self, camera: Camera) -> None:
        particle: Particle
        for particle_index, particle in iter_list_reverse(self.particles):
            if particle.lifespan <= 0:
                del self.particles[particle_index]
                continue

            particle.update()
            particle.draw(camera)
