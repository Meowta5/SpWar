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

    def update(self, need_kill):
        '''Обновление объекта'''
        self.animation(self.animation_speed)
        self.killer(need_kill)
