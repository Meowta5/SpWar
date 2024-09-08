
from random import choice
import pygame

import code.function as function
import code.variable as vb
import code.path.image_path as image_path
from code.object import blast

class BlastManager:
    def __init__(self):
        self.blast_group = pygame.sprite.Group()
        self.ship_type = None
        self.sea_area_rect = None
        
        self.bullet_blast = ()

        self.player_ship_blast = ()
        
        self.asteroid_blast = {
            'small': (),
            'medium': (),
            'big': ()
        }

    def import_blast_image(self):
        '''Импорт изображений взрывов'''
        
        match self.ship_type:
            case 'damnium':
                self.bullet_blast = (
                    function.load_gif(image_path.bullet_blast_one_path,
                                    vb.background_size_coeff * 0.125),
                    function.load_gif(image_path.bullet_blast_two_path,
                                    vb.background_size_coeff * 0.125)
                )
                
                self.player_ship_blast = (function.load_gif(image_path.ship_blast_path_one,
                                                          vb.background_size_coeff * 1.5))
                
            case 'libra':
                self.bullet_blast = (
                    function.load_gif(image_path.bullet_blast_one_path,
                     vb.background_size_coeff * 0.125),
                    function.load_gif(image_path.bullet_blast_two_path,
                     vb.background_size_coeff * 0.125)
                )
                
                self.player_ship_blast = (function.load_gif(image_path.ship_blast_path_one,
                                                          vb.background_size_coeff * 1.5))
                
            case 'celeritas':
                self.bullet_blast = (
                    function.load_gif(image_path.bullet_blast_one_path,
                     vb.background_size_coeff * 0.125),
                    function.load_gif(image_path.bullet_blast_two_path,
                     vb.background_size_coeff * 0.125)
                )
                
                self.player_ship_blast = (function.load_gif(image_path.ship_blast_path_one,
                                                          vb.background_size_coeff * 1.5))
                
            case 'versi':
                self.bullet_blast = (
                    function.load_gif(image_path.bullet_blast_one_path,
                     vb.background_size_coeff * 0.125),
                    function.load_gif(image_path.bullet_blast_two_path,
                     vb.background_size_coeff * 0.125)
                )
                
                self.player_ship_blast = (function.load_gif(image_path.ship_blast_path_one,
                                                          vb.background_size_coeff * 1.5))
                
        self.asteroid_blast['small'] = (
            function.load_gif(image_path.asteroid_blast_one_path, 1),
        )
        self.asteroid_blast['medium'] = (
            function.load_gif(image_path.asteroid_blast_one_path, 1),
        )
        self.asteroid_blast['big'] = (
            function.load_gif(image_path.asteroid_blast_one_path, 1),
        )
    
    def create_bullet_blast(self, size, position, speed):
        '''Создает взрыв снаряда'''

        image_list = []
        for i in choice(self.bullet_blast):
            image_list.append(
                pygame.transform.rotozoom(i, 0, size)
            )
        
        self.blast_group.add(blast.Blast(self.sea_area_rect, image_list, position, speed))

    def create_asteroid_blast(self, asteroid_type, size, position, speed):
        '''Создает взрыв астероида'''
        
        image_list = []
        for i in choice(self.asteroid_blast[asteroid_type]):
            image_list.append(
                pygame.transform.rotozoom(i, 0, size)
            )
        
        self.blast_group.add(blast.Blast(self.sea_area_rect, image_list, position, speed))
    
    def create_player_blast(self, position, speed):
        '''Создает взрыв игрока'''
        self.blast_group.add(blast.Blast(self.sea_area_rect,
                                         self.player_ship_blast, position, speed))

    def update(self):
        '''Обновление взрыва'''
        self.blast_group.update()
    
    def draw(self, screen):
        '''Отрисовка взрыва'''
        self.blast_group.draw(screen)
    
    def start(self, ship_type, sea_area_rect):
        '''Инициализая и импорт всего необходимого для нормальной работы менеджера'''
        self.ship_type = ship_type
        self.sea_area_rect = sea_area_rect
        self.import_blast_image()

