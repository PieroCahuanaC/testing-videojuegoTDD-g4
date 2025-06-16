# card_ui.py
import os
import pygame
from card import Card  # Importa la clase lógica

CARD_SIZE = (100, 140)
ASSETS_DIR = "assets/cards"
CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "card_back.png")), CARD_SIZE)

class VisualCard(Card):
    def __init__(self, name, pos):
        super().__init__(name)  # Inicializa la lógica
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(ASSETS_DIR, f"{name}.png")), CARD_SIZE
        )
        self.rect = pygame.Rect(pos[0], pos[1], CARD_SIZE[0], CARD_SIZE[1])

    def draw(self, screen):
        if self.revealed or self.matched:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(CARD_BACK, self.rect)

    def flip(self):
        if not self.matched:
            self.revealed = not self.revealed
