# main.py

import pygame
from src.game_manager import GameManager
from src.settings import WIDTH, HEIGHT, CARD_SIZE, CARD_BACK, HEART_IMG, SETTINGS_IMG, BACKGROUND_IMG, CARD_NAMES, MAX_LIVES, GAP, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Match Game")
    
    game = GameManager(screen)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    main()
