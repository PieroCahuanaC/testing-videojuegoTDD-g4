# src/confetti.py

import pygame
import random

WIDTH = 800
HEIGHT = 600

class ConfettiParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.size = random.randint(4, 8)
        self.color = random.choice([(94, 86, 227), (3, 217, 195), (204, 0, 0)])
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
