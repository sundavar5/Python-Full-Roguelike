import pygame
import random
from roguelike.config import TILE_SIZE

class Particle:
    def __init__(self, x, y, color, life, dx, dy, size=2):
        self.x = x
        self.y = y
        self.color = color
        self.life = life
        self.max_life = life
        self.dx = dx
        self.dy = dy
        self.size = size

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def is_dead(self):
        return self.life <= 0

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_hit_effect(self, x, y, color=(255, 0, 0)):
        # Convert grid coords to pixel coords (center of tile)
        px = x * TILE_SIZE + TILE_SIZE // 2
        py = y * TILE_SIZE + TILE_SIZE // 2

        for _ in range(10):
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            life = random.randint(10, 20)
            self.particles.append(Particle(px, py, color, life, dx, dy, size=random.randint(2, 4)))

    def add_block_effect(self, x, y):
        px = x * TILE_SIZE + TILE_SIZE // 2
        py = y * TILE_SIZE + TILE_SIZE // 2

        for _ in range(5):
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            life = random.randint(5, 15)
            self.particles.append(Particle(px, py, (200, 200, 255), life, dx, dy))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if not p.is_dead()]

    def draw(self, screen, camera_x, camera_y):
        for p in self.particles:
            screen_x = int(p.x - camera_x)
            screen_y = int(p.y - camera_y)

            # Fade out
            alpha = int((p.life / p.max_life) * 255)
            s = pygame.Surface((p.size, p.size), pygame.SRCALPHA)
            s.fill((*p.color, alpha))
            screen.blit(s, (screen_x, screen_y))
