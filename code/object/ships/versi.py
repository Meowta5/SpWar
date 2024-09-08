
# Все классы связнанные с Верси

import math
from random import randint

import pygame

from code.object import game_object, playership, bullet, light
import code.function as function
import code.variable as vb
import code.path.image_path as image_path


class VersiLight(light.Light):
    def __init__(self, position, image_tuple):
        super().__init__(image_tuple, position)

    def update(self, position, player_angle_state, light_live):
        '''Обновление'''
        self.killer(light_live)
        self.animation()
        self.rotate_behind_object(position, player_angle_state)
        

class VersiLaser(game_object.GameObject):
    def __init__(self, image_tuple, position):
        super().__init__(image_tuple, position)

        self.image = self.image_tuple[0]
        self.rect = self.image.get_rect(midleft=position)

        self.original_image = self.image
        self.original_rect = self.rect
        self.image_index = 0
        self.angle = 0
        base_player_image = function.load_gif(image_path.versi_ship_path, vb.background_size_coeff * 0.5)[0]

        base_player_rect = base_player_image.get_rect(center=(0, 0))

        self.player_circle_radius = (base_player_rect.center[0] - base_player_rect.midright[0]) + (self.rect.center[0] - self.rect.midright[0]) + 10

    def rotate(self, player_rect, angle):
        '''Вращение лазера'''
        
        # Круг координат лазера
        laser_point = self.create_coordinate_circle(self.player_circle_radius, player_rect.center)[int(-angle)]

        self.image, self.rect = self.rotate_image(self.original_image, self.original_rect, -angle)
        self.rect.center = (laser_point[0], laser_point[1])

    def versi_laser_killer(self, laser_live):
        '''Уничтожение лазера игрока'''
        if not laser_live:
            self.kill()

    def update(self, player_rect, angle, living):
        '''Обновление лазера'''
        self.versi_laser_killer(living)
        self.animation()
        self.rotate(player_rect, angle)


class Turret(game_object.GameObject):
    def __init__(self, blast_manager, player_rect, image_tuple):
        super().__init__(image_tuple, player_rect.center)

        # Группа снарядов
        self.bullet_group = pygame.sprite.Group()

        # Задержка выстрелов
        self.shoot_time = 45
        self.turret_bullet_image = function.load_image(image_path.versi_turret_bullet_path,
                                                     vb.background_size_coeff * 0.06)

        # Взрыв снаряда
        self.blast_manager = blast_manager
        
        self.blast_data_tuple = (
            self.blast_manager, # Менеджер
            vb.background_size_coeff * 3.5, # Размер изображения
            1.25 # Скорость анимации
        )
        
    def turret_killer(self, turret_live):
        '''Уничтожение турели'''
        if not turret_live:
            self.kill()

    def turret_move(self, player_rect, player_angle):
        '''Движение турели'''
        self.rect.center = self.create_coordinate_circle((vb.bottomright_main_screen[0] * 0.125) * 0.0525,
                                                 player_rect.center)[int(-player_angle)]

    def turret_ai(self, asteroid_group):
        '''ИИ турели'''
        min_distance = float('inf')
        try:
            for asteroid in asteroid_group:
                distance = math.sqrt(abs(self.rect.centerx - asteroid.rect.centerx) ** 2 + abs(
                    self.rect.centery - asteroid.rect.centery) ** 2)

                if min_distance > distance:
                    min_distance = distance
                    nearest_asteroid = asteroid

            self.bullet_angle = -self.angle_towards_position(self.rect, nearest_asteroid.rect.center)
            self.image, self.rect = self.rotate_image(self.original_image, self.rect, self.bullet_angle)

            if self.shoot_time == 0:
                self.gun_position = self.create_coordinate_circle(((vb.bottomright_main_screen[1] * 0.12)
                                                                   * 0.4449),
                                                                  self.rect.center,
                                                                  switch_lists_use=False)[int(self.bullet_angle)]

                self.bullet_group.add(bullet.Bullet(self.blast_data_tuple, self.turret_bullet_image, asteroid_group,
                                                    self.gun_position, self.bullet_angle, function.ratio_value(15), 3))
                self.shoot_time = 75
            else:
                self.shoot_time -= 1
        except:
            self.image, self.rect = self.rotate_image(self.original_image, self.rect, 0)
        
    def update(self, player_rect, player_angle, asteroid_group, turret_live):
        '''Обновление'''
        self.asteroid_group = asteroid_group

        self.turret_killer(turret_live)
        self.turret_ai(asteroid_group)
        self.turret_move(player_rect, player_angle)

        self.bullet_group.update(self.asteroid_group)


class VersiShip(playership.PlayerShip):
    def __init__(self, blast_manager, image_tuple, position, player_speed,
                 player_damage, shoot_basic_recharge_time, shield_repair_speed, shield, health):
        super().__init__(blast_manager, image_tuple, position, player_speed, player_damage, shield_repair_speed, shield, health)

        # Компоненты Верси
        # Свет
        self.light_group.add(VersiLight(self.rect.center, function.load_gif(image_path.versi_light_path, vb.background_size_coeff)))

        # Лазер
        self.laser_group = pygame.sprite.GroupSingle()

        self.laser_group.add(VersiLaser(function.load_gif(image_path.versi_laser_path, vb.background_size_coeff),
                                        self.rect.midright))

        self.laser_draw = False
        self.laser_one_call = True
        self.laser_living_time = 0
        self.shoot_recharge_time = 0
        self.shoot_basic_recharge_time = shoot_basic_recharge_time * 30
        
        self.turret_group = pygame.sprite.GroupSingle()
        self.turret_group.add(
            Turret(self.blast_manager, self.rect,
                   function.load_image(image_path.versi_turret_path,
                                     vb.background_size_coeff * 0.55))
        )
        
    def versi_shoot(self):
        '''Стрельба'''
        keys = pygame.key.get_pressed()

        self.shoot_recharge_time -= 1

        # Проверка на нажатие пробела
        if keys[pygame.K_SPACE]:
            # Проверка живет ли лазер меньше 90 итераций цикла (3 секунды)
            if self.laser_living_time < 90:
                if self.shoot_recharge_time <= 0:
                    self.laser_living_time += 1
                    if self.laser_one_call:
                        # Включение отрисовки лазера
                        self.laser_draw = True
                        self.laser_one_call = False

                    # Проверка на столкновение с астероидом
                    for asteroid in self.asteroid_group:
                        if pygame.sprite.spritecollide(asteroid, self.laser_group, dokill=False):
                            asteroid.receiv_damage(self.player_damage)

            else:
                # Если лазер живет более 90 итераций цикла (3 секунды) то тогда больше его не ресуем его
                self.laser_draw = False
                self.laser_living_time = 0
                self.laser_one_call = True
                self.shoot_recharge_time = self.shoot_basic_recharge_time

        else:
            # Если пробел отжат не ресуем лазер
            if not self.laser_one_call:
                self.laser_draw = False
                self.laser_living_time = 0
                self.laser_one_call = True
                self.shoot_recharge_time = self.shoot_basic_recharge_time

    def versi_killer(self):
        '''Уничтожение верси и всех объектов'''
        if not self.ship_live:
            self.light_group.update(self.rect.center, self.player_ship_move_state, False)
            self.laser_group.update(self.rect, self.angle, False)
            self.turret_group.update(self.rect, self.angle, self.asteroid_group, False)
            self.kill()
            return True
        return False

    def update(self, asteroid_group, player_ship_move_state):
        '''Обновление'''
        self.player_ship_move_state = player_ship_move_state
        self.asteroid_group = asteroid_group
        
        if not self.versi_killer():
            self.animation()
            self.collision_asteroid()
            self.move()
            
            self.versi_shoot()
            self.repair_shield()
            self.update_ship_has()
            
            # Компоненты Верси
            self.light_group.update(self.rect.center, self.player_ship_move_state, True)
            self.laser_group.update(self.rect, self.angle, True)
            self.turret_group.update(self.rect, self.angle, asteroid_group, True)
