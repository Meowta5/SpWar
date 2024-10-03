import pygame

from code.object import game_object


class StaticObject(game_object.GameObject):
    def __init__(self, image_data, position, animation_speed):
        super().__init__(image_data, position)

        if type(image_data) == list or type(image_data) == tuple:
            self.update = self.animation_update
        elif type(image_data) == pygame.Surface:
            self.update = self.static_update

        self.animation_speed = animation_speed

    def killer(self, need_kill):
        '''Уничтожает объект'''
        if need_kill:
            self.kill()

    def get_rect(self):
        '''Возвращает прямоугольник объекта'''
        return self.rect

    def set_rect(self, rect):
        '''Устанавливает прямоугольник объекта'''
        self.rect = rect

    def set_center_position(self, position):
        '''Перемещает центр объекта'''
        self.rect.center = position

    def move(self, x, y) -> tuple:
        '''
        Добавляет к координатам x и y указанные значения.
        Возвращает новые координаты центра объекта
        '''
        self.rect.x += x
        self.rect.y += y
        return self.rect.center

    def animation_update(self, need_kill, screen_rect):
        '''Обновление и анимация объекта'''
        self.killer(need_kill)
        if self.rect.colliderect(screen_rect):
            self.animation(self.animation_speed)

    def static_update(self, need_kill):
        '''Обновление объекта'''
        self.killer(need_kill)

    def update(self):
        ...
