import pygame
import os

# Dimensiones de la pantalla y configuraciones generales
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_SIZE = (100, 140)
GAP = 20
MAX_LIVES = 5

# Ruta de assets
ASSETS_DIR = "assets/cards"

# Nombres de las cartas disponibles
CARD_NAMES = ["apple", "banana", "cherry", "grape", "lemon", "orange"]

# Carga de imágenes
CARD_BACK = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "card_back.png")),
    CARD_SIZE
)

HEART_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "heart.png")),
    (40, 40)
)

SETTINGS_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "ajustes.png")),
    (50, 50)
)

BACKGROUND_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_DIR, "fondo.png")),
    (WIDTH, HEIGHT)
)
