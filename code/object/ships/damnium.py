
# Все классы связнанные с Дамниумом
from code.object import playership, light

import code.function as function
import code.variable as vb
import code.path.image_path as image_path


class DamniumLight(light.Light):
    def __init__(self, position, image_tuple):
        super().__init__(image_tuple, position)

    # Обновление
    def update(self, position, player_angle_state, light_live):
        self.killer(light_live)
        self.animation()
        self.rotate_behind_object(position, player_angle_state)


class DamniumShip(playership.PlayerShip):
    def __init__(self, blast_manager, image_tuple, position, player_speed, player_damage, shoot_basic_recharge_time,
                 shoot_standart_move, shield_repair_speed, shield, health):
        super().__init__(blast_manager, image_tuple, position, player_speed, player_damage, shield_repair_speed, shield, health)

        # Параметры Дамниума
        
        # Стрельба
        self.shoot_standart_move = shoot_standart_move
        self.shoot_move = 0
        self.shoot_move_direction = 0
        self.shoot_basic_recharge_time = shoot_basic_recharge_time
        # Компоненты Дамниума
        
        # Снаряд
        
        # Картеж картинок
        self.bullet_image_tuple = function.load_image(image_path.damnium_bullet_path, vb.background_size_coeff * 0.15)
        self.bullet_speed = function.ratio_value(15)
        
        # Взрыв снаряда
        self.blast_data_tuple = (
            self.blast_manager, # Менеджер
            vb.background_size_coeff * 7.5, # Размер изображения
            1 # Скорость анимации
        )
        
        # Свет
        self.light_group.add(DamniumLight(self.rect.center, function.load_gif(image_path.damnium_light_path, vb.background_size_coeff)))

    def damnium_killer(self):
        '''Уничтожения Дамниума'''
        if not self.ship_live:
            self.light_group.update(self.rect.center, self.player_ship_move_state, False)
            self.kill()

    def update(self, asteroid_group, player_ship_move_state):
        '''Обновление'''
        self.player_ship_move_state = player_ship_move_state
        self.asteroid_group = asteroid_group
        
        self.damnium_killer()
        self.animation()
        self.collision_asteroid()
        self.move()
        
        self.shoot(self.rect.center)
        self.repair_shield()
        self.update_ship_has()
        self.bullet_group.update(self.asteroid_group)
        
        # Компоненты Дамниума
        self.light_group.update(self.rect.center, self.player_ship_move_state, True)
