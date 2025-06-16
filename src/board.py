import random
import os
import pygame
from src.card import Card

# Configuración del tablero
CARD_SIZE = (100, 140)
GAP = 20
ROWS, COLS = 3, 4
CARD_NAMES = ["apple", "banana", "cherry", "grape", "lemon", "orange"]
ASSETS_DIR = "assets/cards"

def create_board():
    card_names = CARD_NAMES * 2  # crear pares
    random.shuffle(card_names)
    board = []

    total_width = COLS * CARD_SIZE[0] + (COLS - 1) * GAP
    total_height = ROWS * CARD_SIZE[1] + (ROWS - 1) * GAP
    offset_x = (800 - total_width) // 2
    offset_y = 100

    for row in range(ROWS):
        for col in range(COLS):
            x = offset_x + col * (CARD_SIZE[0] + GAP)
            y = offset_y + row * (CARD_SIZE[1] + GAP)
            board.append(Card(card_names.pop(), (x, y)))
    return board
