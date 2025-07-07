# src/card_ui.py
import pygame
from .card import Card
from .settings import WIDTH, HEIGHT, CARD_SIZE, CARD_BACK, HEART_IMG, SETTINGS_IMG, BACKGROUND_IMG, CARD_NAMES, MAX_LIVES, GAP, FPS

class CardUI:
    def __init__(self, card: Card, rect):
        self.card = card
        self.rect = rect
        
        self.image = pygame.transform.scale(card.image, CARD_SIZE)

    def draw(self, screen):
        if self.card.is_flipped or self.card.is_matched:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(CARD_BACK, self.rect)
