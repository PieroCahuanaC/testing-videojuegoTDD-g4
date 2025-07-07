import pygame
import os
from .settings import CARD_SIZE

ASSETS_DIR = "assets/cards"

class Card:
    def __init__(self, card_id, image=None):
        self.id = card_id
        self.name = card_id
        self.image = image or self.load_image(card_id)
        self.revealed = False
        self.matched = False

    @property
    def is_flipped(self):
        return self.revealed

    @property
    def is_matched(self):
        return self.matched

    def load_image(self, card_id):
        try:
            image_path = os.path.join(ASSETS_DIR, f"{card_id}.png")
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, CARD_SIZE)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la imagen de la carta '{card_id}': {e}")
            return pygame.Surface(CARD_SIZE)  # Imagen vacía por defecto

    def reveal(self):
        if not self.matched:
            self.revealed = True

    def hide(self):
        if not self.matched:
            self.revealed = False

    def match(self):
        self.matched = True

    def is_match(self, other_card):
        return self.id == other_card.id
    
    def flip(self):
        if not self.matched:
            self.revealed = not self.revealed

    @property
    def is_matched(self):
        return self.matched

    @is_matched.setter
    def is_matched(self, value):
        self.matched = value
