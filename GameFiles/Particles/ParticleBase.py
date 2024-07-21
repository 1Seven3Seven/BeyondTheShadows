from abc import ABC, abstractmethod


class ParticleBase(ABC):
    def __int__(self, x: int, y: int, radius: float, vx: float, vy: float, lifespan: int):
        self.x = x
        self.y = y
        self.radius = radius

        self.vx = vx
        self.vy = vy

        self.lifespan = lifespan

    def move(self):
        self.x += self.vx
        self.y += self.vy

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError
