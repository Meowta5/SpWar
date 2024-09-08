
#

import pygame

import code.variable as vb
import code.json_function as json_func
import code.path.json_path as json_path

class ScreenManager:
    def __init__(self):
        
        # Создание окна
        self.screen = pygame.display.set_mode(vb.screen_size)
        
        # Имя окна
        pygame.display.set_caption('SpWar')

        self.screen_size_index = vb.settings['screen_size_index']
        
    def screen_resolution_change(self, index: int) -> pygame.surface.Surface:
        '''Изменение размеров экрана'''
        match index:
            case 0:
                screen_width = 1200
                screen_height = 600
            case 1:
                screen_width = 1400
                screen_height = 700
            case 2:
                screen_width = 1600
                screen_height = 800
            case 3:
                screen_width = 1800
                screen_height = 900
            case 4:
                screen_width, screen_height = vb.DISPLAY_SIZE
            
        window_position = ((vb.DISPLAY_SIZE[0] - screen_width) // 2,
                           (vb.DISPLAY_SIZE[1] - screen_height) // 2)
            
        vb.settings['screen_size_index'] = index
        self.screen_size_index = index
        json_func.write(vb.settings, json_path.settings)
        vb.screen_resolution_update()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_window_position(window_position)
        return (screen_width, screen_height)
    
    def get_screen(self) -> pygame.surface.Surface:
        '''Возвращает поверхность окна'''
        return self.screen

    def get_screen_size_index(self):
        '''Возвращает индекс размеров окна'''
        return self.screen_size_index
    