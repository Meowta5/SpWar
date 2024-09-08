
# Класс астероидов
from random import randint

import pygame

import code.variable as vb

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, blast, image, angle_speed, speed, health):
        super().__init__()
        
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(midright=(-10, -10))
        self.mask = pygame.mask.from_surface(self.image)
        
        self.health = health

        self.need_kill = False
        
        self.angle_speed = angle_speed
        self.speed = speed
        self.rotate_angle = 0
        
        self.blast_manager, self.asteroid_type, self.size = blast

    def rotate_image(self, image, image_rect, angle):
        '''Поворот изображения на определенный угол'''
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        return rotated_image, rotated_rect

    def teleport_position(self, position):
        '''Телепортация астероида в определенную позицию'''
        self.rect.center = position

    def return_rect(self):
        '''Возвращает прямоугольник астероида'''
        return self.rect

    def rotate_animation(self):
        '''Поворот астероида'''
        self.image, self.rect = self.rotate_image(self.original_image, self.rect, self.rotate_angle)
        self.rotate_angle += self.angle_speed

        self.mask = pygame.mask.from_surface(self.image)
        if self.rotate_angle >= 360:
            self.rotate_angle = 0

    def move(self):
        '''Движение астероида'''
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.rect.x = vb.bottomright_main_screen[0] + abs(self.rect.centerx - self.rect.right) * float(
                f'{randint(1, 2)}.{randint(5, 9)}{randint(5, 9)}{randint(5, 9)}{randint(5, 9)}{randint(5, 9)}')

    def check_health(self):
        '''Проверка прочности астероида'''
        if self.health <= 0 or self.need_kill:
            self.blast_manager.create_asteroid_blast(
                self.asteroid_type,
                self.size * 4,
                self.rect.center,
                float(f'0.{randint(5, 7)}{randint(0, 9)}')
            )
            self.kill()

    def receiv_damage(self, damage):
        '''Получение урона'''
        self.health -= damage
        if self.health < 0:
            self.need_kill = True
            return abs(self.health)
        
        elif self.health == 0:
            self.need_kill = True
            
        return False
        
    def update(self, sea_area_rect):
        '''Обновление'''
        self.check_health()
        self.move()
        if sea_area_rect.colliderect(self.rect):
            self.rotate_animation()
