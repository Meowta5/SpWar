
# Класс снаряда
import math
import random
import pygame

from code.object import game_object
import code.variable as vb

class Bullet(game_object.GameObject):
    def __init__(self, blast, image, asteroid_group, position, angle, move_speed, damage):
        super().__init__(image, position)

        self.blast_manager, self.size, self.blast_animation_speed = blast

        # Параметры снаряда
        self.angle = math.radians(angle)
        self.speed = move_speed + ((move_speed / 100) * random.randint(-3, 3))
        self.damage = damage
        self.rotate_angle = 0
        self.living_time = 0

        # Группа астероидов
        self.asteroid_group = asteroid_group
        
        # Скорость по координатам x, y
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)

        # Время жизни
        self.time_live_max = vb.bottomright_main_screen[0] / (abs(self.speed_x) + abs(self.speed_y)) * 1.35
    
    def collision(self):
        '''Столкновение астероидов и снарядов'''
        for asteroid in self.asteroid_group:
            if self.rect.colliderect(asteroid.rect):
                
                # Вычисление оффсета
                offset = (asteroid.rect.topleft[0] - self.rect.left, asteroid.rect.topleft[1] - self.rect.top)
                
                # Проверка на столкновение масок
                if self.mask.overlap_area(asteroid.mask, offset):
                    excess_damage = asteroid.receiv_damage(self.damage)
                    asteroid.check_health()
                    
                    if excess_damage:
                        self.damage = excess_damage
                    else:
                        self.blast_manager.create_bullet_blast(self.size,
                                                               self.rect.center,
                                                               self.blast_animation_speed)
                        self.kill()

    def bullet_move(self):
        '''Движение пуль'''
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y

    def bullet_animation(self):
        '''Анимация снаряда'''
        self.rotate_angle += 5
        if self.rotate_angle >= 360:
            self.rotate_angle = 0
        self.image, self.rect = self.rotate_image(self.original_image, self.rect, self.rotate_angle)

    def bullet_killer(self):
        '''Уничтожение пуль'''
        if self.living_time >= self.time_live_max:
            self.kill()
        else:
            self.living_time += 1

    def update(self, asteroid_group):
        '''Обновление снаряда'''
        self.asteroid_group = asteroid_group
        
        self.collision()
        self.bullet_move()
        self.bullet_animation()
        self.bullet_killer()
