
import pygame
pygame.init()

from code.managers.game_manager import GameManager

#-------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.run_game()
#-------------------------------------------------------------------------------------------------#
