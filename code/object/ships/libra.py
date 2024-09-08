
# Все классы связнанные с Либрой
import pygame

from code.object import playership, light

import code.function as function
import code.variable as vb
import code.path.image_path as image_path


class LibraLight(light.Light):
    def __init__(self, position, image_tuple):
        super().__init__(image_tuple, position)
    
    def update(self, position, player_angle_state, light_live):
        '''Обновление'''
        self.killer(light_live)
        self.animation()
        self.rotate_behind_object(position, player_angle_state)


class LibraShip(playership.PlayerShip):
    def __init__(self, blast_manager, image_tuple, position, player_speed, player_damage, shoot_basic_recharge_time,
                 shoot_standart_move, shield_repair_speed, shield, health):
        super().__init__(blast_manager, image_tuple, position, player_speed, player_damage, shield_repair_speed, shield, health)
        
        # Параметры Либры
        self.shoot_standart_move = shoot_standart_move
        self.shoot_move = 0
        self.shoot_move_direction = 0
        self.shoot_basic_recharge_time = shoot_basic_recharge_time
        self.gun_pos_coeff = -85
        
        # Компоненты Либры
        
        # Снаряд
        
        # Изображение
        self.bullet_image_tuple = pygame.transform.rotozoom(
            pygame.image.load(image_path.libra_bullet_path),
            0, vb.background_size_coeff * 0.075
        )
        
        self.bullet_speed = function.ratio_value(15)
        
        # Взрыв снаряда
        self.blast_data_tuple = (
            self.blast_manager, # Менеджер
            vb.background_size_coeff * 3.5, # Размер изображения
            0.85 # Скорость анимации
        )
        
        # Свет
        self.light_group.add(LibraLight(self.rect.center, function.load_gif(image_path.libra_light_path, vb.background_size_coeff)))
        
    def libra_killer(self):
        '''Уничтожение либры'''
        if not self.ship_live:
            self.light_group.update(self.rect.center, self.player_ship_move_state, False)
            self.kill()
    
    def libra_shoot(self):
        '''Стрельба'''
        circle = self.create_coordinate_circle(279 * (vb.background_size_coeff * 0.5), self.rect.center)
        ddd = self.shoot(circle[int(-self.angle) + self.gun_pos_coeff])
        if not ddd is None:
            self.gun_pos_coeff = ddd

    def update(self, asteroid_group, player_ship_move_state):
        '''Обновление'''        
        self.player_ship_move_state = player_ship_move_state
        self.asteroid_group = asteroid_group
        
        self.libra_killer()
        self.animation()
        self.collision_asteroid()
        self.move()
        
        self.libra_shoot()
        self.repair_shield()
        self.update_ship_has()
        self.bullet_group.update(self.asteroid_group)
        
        # Компоненты Либры
        self.light_group.update(self.rect.center, self.player_ship_move_state, True)
