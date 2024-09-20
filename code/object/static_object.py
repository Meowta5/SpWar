import pygame

from code.object import game_object


class StaticObject(game_object.GameObject):
    def __init__(self, image_tuple, position, animation_speed):
        super().__init__(image_tuple, position)
        self.animation_speed = animation_speed

    def killer(self, need_kill):
        '''Уничтожает объект'''
        if need_kill:
            self.kill()

    def get_rect(self):
        '''Возвращает прямоугольник объекта'''
        return self.rect
    
    def move(self, position):
        '''Перемещает центр объекта'''
        self.rect.center = position

    def update(self, need_kill, screen_rect):
        '''Обновление объекта'''
        self.killer(need_kill)
        if self.rect.colliderect(screen_rect):
            self.animation(self.animation_speed)
