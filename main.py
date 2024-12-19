import pygame
from game_logic.game_manager import Game

if __name__== "__main__":
    pygame.mixer.init()
    pygame.init()
    game = Game()
    game.run()