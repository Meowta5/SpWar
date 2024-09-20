
from random import randint, choice
from sys import exit

import pygame

import code.variable as vb
import code.word as word

import code.path.image_path as image_path
from code.managers import space_manager, gui_manager, screen_manager
import code.path.json_path as json_path
import code.json_function as json_func

class GameManager:
    def __init__(self):
        super().__init__()
        
        self.screen_manager = screen_manager.ScreenManager()
        _, self.screen = self.screen_manager.get_screen()
        
        # Отображения логотипа игры при загрузке
        self.load_screen_image = pygame.transform.scale(pygame.image.load(image_path.load_screen_path),
                                                        vb.bottomright_main_screen)
        self.load_screen_rect = self.load_screen_image.get_rect(topleft=(0, 0))
        
        self.screen.blit(self.load_screen_image, self.load_screen_rect)
        pygame.display.update() 
        
        # Ограничение скорости цикоа событий
        self.clock = pygame.time.Clock()

        # Состояние игры
        self.game_status = False

        # Графический интерфейс менеджер
        self.gui_manager = gui_manager.GUIManager(self.screen_manager, self.clock)
        self.gui_manager.start(self.gui_manager)
        
        # Космический менеджер
        self.space_manager = space_manager.SpaceManager(self.clock)
        
    def run_game(self):
        while True:
            self.gui_manager.run_gui()
            