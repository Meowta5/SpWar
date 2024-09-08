
import pygame

import code.function as function
import code.variable as vb
import code.path.image_path as image_path
from code.object import spacebackground, pause
from code.managers import asteroid_manager, blast_manager, player_ship_manager

class SpaceManager:
    def __init__(self, clock):
        
        # Пауза
        self.pause_game = False
        self.pause_space_timer = 0
        self.pause_space_group = pygame.sprite.GroupSingle()
        self.pause_space_group.add(pause.PauseBackground())
        
        # Создание менеджеров
        self.blast_manager = blast_manager.BlastManager()
        self.asteroid_manager = asteroid_manager.AsteroidManager(clock)
        self.player_ship_manager = player_ship_manager.PlayerShipManager()

    def create_background(self, background_path: str):
        '''Создание фона'''
        
        self.background_group = pygame.sprite.Group()
        
        self.background_group.add(spacebackground.SpaceBackground(
            pygame.transform.rotozoom(pygame.image.load(background_path),
                                      0, vb.background_size_coeff),
            (vb.bottomright_main_screen[0],
            vb.topleft_main_screen[1]))
        )

        self.background_group.add(spacebackground.SpaceBackground(
            pygame.transform.rotozoom(pygame.image.load(background_path), 0,
                                      vb.background_size_coeff), vb.topleft_main_screen)
        )
    
    def space_play(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if self.pause_space_timer <= 0:
                self.pause_game = not self.pause_game
                self.pause_space_timer = 15
        else:
            self.pause_space_timer -= 1
            
        if not self.pause_game:
            # Обновление объектов
            self.background_group.update()
            self.player_ship_manager.update(self.asteroid_manager.asteroid_group)
            self.blast_manager.update()
            
            self.asteroid_manager.update(self.sea_area_rect)
            self.asteroid_manager.asteroid_generator()
        
        self.background_group.draw(self.screen)
        self.asteroid_manager.draw(self.screen)
        self.blast_manager.draw(self.screen)
        self.player_ship_manager.draw(self.screen)
        
        if self.pause_game:
            self.pause_space_group.draw(self.screen)
    
    def start(self, type_ship):
        
        # Видимая область
        self.sea_area_rect = pygame.Rect(vb.topleft_main_screen,
                                            vb.bottomright_main_screen)
        
        # Создание фона
        self.create_background(image_path.background_path_one)
        
        # Стар менеджеров
        self.blast_manager.start(type_ship, self.sea_area_rect)
        self.asteroid_manager.start(self.blast_manager)
        self.player_ship_manager.start(self.blast_manager)
        
        # Создание игрока
        self.player_ship_manager.create_player_ship(
                                self.blast_manager,
                                type_ship, # Тип корабля
                                function.ratio_value(20), # Скорость игрока
                                10, # Урон Игрока
                                0, # Перезарядка игрока
                                function.ratio_value(10), # Отдача при выстреле
                                3, # Восстановление щита
                                100, # Щит
                                1) # Прочность
        