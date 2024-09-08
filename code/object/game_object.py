
# Класс игрового объекта

import math

import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_data, position):
        super().__init__()
        
        if type(image_data) == list or type(image_data) == tuple:
            self.image_tuple = image_data
            
            mask_list = []
            for i in self.image_tuple:
                mask_list.append(pygame.mask.from_surface(i))
            
            self.mask_tuple = tuple(mask_list)
            self.mask = self.mask_tuple[0]

            self.original_image = image_data[0]
            self.original_rect = self.original_image.get_rect(center=position)

            self.image = self.original_image
            self.rect = self.original_rect

            self.image_tuple_len = len(self.image_tuple) - 1
            self.image_index = 0
        
        elif type(image_data) == pygame.Surface:
            self.original_image = image_data
            self.original_rect = self.original_image.get_rect(center=position)
            
            self.image = self.original_image
            self.rect = self.original_rect
            self.mask = pygame.mask.from_surface(self.image)

    def animation(self, speed=0.55):
        '''Покадровая анимация объекта'''
        self.image = self.image_tuple[int(self.image_index)]
        self.original_image = self.image_tuple[int(self.image_index)]
        self.mask = self.mask_tuple[int(self.image_index)]
        self.image_index += speed
        if self.image_index >= self.image_tuple_len:
            self.image_index = 0

    def rotate_towards_cursor(self, image, image_rect):
        '''Поворот изображения в сторону курсора'''
        cursor_pos = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(cursor_pos[1] - image_rect.centery, cursor_pos[0] - image_rect.centerx))
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        return rotated_image, rotated_rect

    def rotate_image(self, image, image_rect, angle):
        '''Поворот изображения на определенный угол'''
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)
        return rotated_image, rotated_rect

    def angle_towards_cursor(self, rect):
        '''Вычисление угла относительно центра квадрата и позиции курсора'''
        cursor_pos = pygame.mouse.get_pos()
        return math.degrees(math.atan2(rect.centery - cursor_pos[1], cursor_pos[0] - rect.centerx))

    def angle_towards_position(self, rect, position):
        '''Вычисление угла относительно центра квадрата и позиции'''
        return math.degrees(math.atan2(rect.centery - position[1], position[0] - rect.centerx))

    def create_coordinate_circle(self, radius, center, switch_lists_use=True):
        '''Создание круга координат'''
        def switch_lists(lst):
            half = len(lst) // 2
            new_lst = lst[half:] + lst[:half]
            return new_lst

        points = []
        num_points = 360
        angle_increment = 2 * math.pi / num_points
        center_x, center_y = center
        for i in range(num_points):
            angle = i * angle_increment
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            points.append((x, y))

        if switch_lists_use:
            return switch_lists(points)
        else:
            return points
