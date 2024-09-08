
# Класс кнопка

import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image_tuple, position, function, function_args):
        super().__init__()
        self.image_tuple = image_tuple
        self.image = self.image_tuple[0]
        self.rect = self.image.get_rect(topleft=position)
        self.function = function
        self.function_args = function_args
        self.pressed = False

    def function_call(self):
        '''Вызов функции'''
        if pygame.mouse.get_pressed()[0]:
            self.pressed = True
        else:
            if self.pressed:    
                self.function(**self.function_args)
                self.pressed = False
                
    
    def change_texture(self):
        '''Смена картинки в случае если курсор наведен/ не наведен на кнопку'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_tuple[0]
            self.function_call()
        else:
            self.image = self.image_tuple[1]
        
    def update(self):
        self.change_texture()
