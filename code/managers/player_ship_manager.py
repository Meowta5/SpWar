
import pygame

import code.function as function
import code.variable as vb
import code.path.image_path as image_path
from code.object.ships import celeritas, damnium, versi, libra
from code.managers import blast_manager

class PlayerShipManager:
    def __init__(self):
        self.player_ship_group = pygame.sprite.GroupSingle()
        self.player_ship_draw = True
        self.position = (0, 0)
        
        self.blast_manager = None
        
    def create_player_ship(self, blast_manager: blast_manager.BlastManager, ship_type: str, player_speed: float,
                           player_damage: float, shoot_basic_recharge_time: float,
                           shoot_standart_move: float, shield_repair_speed: float,
                           shield: float, health: float):
        
        '''Создание космического корабля игрока'''
        
        choice_ship = {
            'damnium': lambda: damnium.DamniumShip(blast_manager, function.load_gif(image_path.damnium_ship_path, vb.background_size_coeff * 0.5),
                                           (150, 150), player_speed,
                                           player_damage, shoot_basic_recharge_time, shoot_standart_move, shield_repair_speed, shield, health),
            
            'libra': lambda: libra.LibraShip(blast_manager, function.load_gif(image_path.libra_ship_path, vb.background_size_coeff * 0.5),
                                     (300, 300), player_speed,
                                     player_damage, shoot_basic_recharge_time, shoot_standart_move, shield_repair_speed, shield, health),
            
            'celeritas': lambda: celeritas.CeleritasShip(blast_manager, function.load_gif(image_path.celeritas_ship_path, vb.background_size_coeff * 0.25),
                                     (300, 300), player_speed,
                                     player_damage, shoot_basic_recharge_time, shoot_standart_move, shield_repair_speed, shield, health),
            
            'versi': lambda: versi.VersiShip(blast_manager, function.load_gif(image_path.versi_ship_path, vb.background_size_coeff * 0.5),
                                            (300, 300), player_speed,
                                     player_damage, shoot_basic_recharge_time, shield_repair_speed, shield, health)
        }

        def damnium_draw(screen):
            # Отрисовка корабля игрока и его компонентов
            self.player_ship_group.sprite.light_group.draw(screen)
            self.player_ship_group.sprite.bullet_group.draw(screen)
            self.player_ship_group.draw(screen)
            
        def libra_draw(screen):
            # Отрисовка корабля игрока и его компонентов
            self.player_ship_group.sprite.light_group.draw(screen)
            self.player_ship_group.sprite.bullet_group.draw(screen)
            self.player_ship_group.draw(screen)
            
        def celeritas_draw(screen):
            # Отрисовка корабля игрока и его компонентов
            self.player_ship_group.sprite.light_group.draw(screen)
            self.player_ship_group.sprite.bullet_group.draw(screen)
            self.player_ship_group.draw(screen)
            
        def versi_draw(screen):
            # Отрисовка корабля игрока и его компонентов
            self.player_ship_group.sprite.light_group.draw(screen)
            if self.player_ship_group.sprite.laser_draw:
                self.player_ship_group.sprite.laser_group.draw(screen)
            self.player_ship_group.draw(screen)
            self.player_ship_group.sprite.turret_group.sprite.bullet_group.draw(screen)
            self.player_ship_group.sprite.turret_group.draw(screen)
        
        
        if ship_type == 'damnium':
            self.ship_draw = damnium_draw
            
        elif ship_type == 'libra':
            self.ship_draw = libra_draw
            
        elif ship_type == 'celeritas':
            self.ship_draw = celeritas_draw

        elif ship_type == 'versi':
            self.ship_draw = versi_draw
        
        
        self.ship_type = ship_type
        self.player_ship_group.add(choice_ship[ship_type]())

    def update(self, asteroid_group):
        '''Обновление корабля игрока'''
        self.player_ship_group.update(asteroid_group, vb.player_ship_move_state)

    def draw(self, screen):
        '''Отрисовка корабля игрока'''
        if self.player_ship_draw:
            try:
                
                self.ship_draw(screen)
                
                self.player_ship_group.sprite.player_health_and_shield_background_group.draw(screen)
                self.player_ship_group.sprite.player_health_group.draw(screen)
                self.player_ship_group.sprite.player_shield_group.draw(screen)
                self.position = self.player_ship_group.sprite.rect.center
            except AttributeError:
                self.player_ship_draw = False
                self.blast_manager.create_player_blast(self.position, 0.75)
                print('\n\n\nИГРОКУ КАПЕЦ!!!\n\n\n')

    def start(self, blast_manager):
        '''Инициализая и импорт всего необходимого для нормальной работы менеджера'''
        self.blast_manager = blast_manager
