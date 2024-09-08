
# Все классы связанные с игроком

import math
from random import randint, choice

import pygame

from code.object import game_object, bullet

import code.function as function
import code.json_function as json_func
import code.path.json_path as json_path
import code.variable as vb


class ParametersLine(game_object.GameObject):
    def __init__(self, player_rect, player_param, color, position):
        
        # Создание поверхности изображения
        self.image = pygame.transform.rotozoom(pygame.Surface((300, 40)), 0, vb.background_size_coeff)
        self.image.fill(color)
        super().__init__((self.image, self.image), position)
        
        # Создание переменных
        self.circle_radius = player_rect.center[0] - player_rect.right
        self.one_procent_size = 3 * vb.background_size_coeff
        self.player_param = player_param
        self.y_size = 40 * vb.background_size_coeff
        self.need_move_bool = True
        
    def move(self, player_rect, player_angle):
        '''Передвижение прочности игрока'''
        circle = self.create_coordinate_circle(self.circle_radius, player_rect.center)
        self.rect.center = circle[int(-player_angle) + 75]
        self.need_move_bool = True
        
    def define_location(self):
        if self.need_move_bool:
            self.need_move_bool = False
            position = (function.ratio_value(25), function.ratio_value(25))
            self.rect.topleft = position

    def transform_helth(self, player_param):
        '''Изменение размер прочности игрока.
        Например при уменьшении прочности уменьшается размер полоски'''
        self.image = pygame.transform.scale(self.original_image, ((player_param / self.player_param * 100) * self.one_procent_size, self.y_size))
        
    def update(self, player_rect, player_angle, player_param, transform=True):
        if transform:
            self.transform_helth(player_param)
        
        if vb.move_location:
            self.move(player_rect, player_angle)
        else:
            self.define_location()

class PlayerShip(game_object.GameObject):
    def __init__(self, blast_manager, image_tuple, position, player_speed,
                 player_damage, shield_repair_speed, shield, health):
        super().__init__(image_tuple, position)
        
        # Параметры
        self.player_speed = player_speed
        self.player_damage = player_damage
        self.angle = 0

        # Щит и броня
        self.shield = shield
        self.basic_shield = shield
        self.health = health
        self.shield_recovery = True
        self.shield_repair_speed = shield_repair_speed
        
        self.ship_live = True

        # Стрельба
        self.shoot_recharge_time = 0
        self.revers_gun = False

        # Группы
        self.bullet_group = pygame.sprite.Group()
        self.light_group = pygame.sprite.GroupSingle()
        
        # Взрыв
        self.blast_manager = blast_manager
        
        # Прочность и щит
        self.player_health_and_shield_background_group = pygame.sprite.GroupSingle()
        self.player_health_and_shield_background_group.add(ParametersLine(self.rect, None, (0, 0, 0), (150, 250)))
        self.player_health_group = pygame.sprite.GroupSingle()
        self.player_health_group.add(ParametersLine(self.rect, self.health, (255, 0, 0), (150, 250)))
        self.player_shield_group = pygame.sprite.GroupSingle()
        self.player_shield_group.add(ParametersLine(self.rect, self.shield, (0, 0, 255), (150, 250)))

        # Управление
        self.load_controls()
        
    def move_straight(self):
        '''Движение WASD'''
        keys = pygame.key.get_pressed()
        # Движение по оси Y
        if keys[pygame.K_w]:
            self.rect.y -= self.player_speed
            self.y_move = True
        elif keys[pygame.K_s]:
            self.rect.y += self.player_speed
            self.y_move = True
        else:
            self.y_move = False

        # Ограничение по оси Y
        if self.rect.top < vb.topleft_main_screen[1]:
            self.rect.top = vb.topleft_main_screen[1]
        elif self.rect.bottom > vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]:
            self.rect.bottom = vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]

        # Движение по оси X
        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
            self.x_move = True
        elif keys[pygame.K_d]:
            self.rect.x += self.player_speed
            self.x_move = True
        else:
            self.x_move = False

        # Ограничение по оси X
        if self.rect.left <= vb.topleft_main_screen[0]:
            self.rect.left = vb.topleft_main_screen[0]
        elif self.rect.right >= vb.bottomright_main_screen[0]:
            self.rect.right = vb.bottomright_main_screen[0]

    def move_turn_straight(self):
        '''Движение WASD + поворот в сторону мыши'''
        self.image, self.rect = self.rotate_towards_cursor(self.original_image, self.rect)
        keys = pygame.key.get_pressed()

        # Движение по оси Y
        if keys[pygame.K_w]:
            self.rect.y -= self.player_speed
            self.y_move = True
        elif keys[pygame.K_s]:
            self.rect.y += self.player_speed
            self.y_move = True
        else:
            self.y_move = False

        # Ограничение по оси Y
        if self.rect.top <= vb.topleft_main_screen[1]:
            self.rect.top = vb.topleft_main_screen[1]
        elif self.rect.bottom >= vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]:
            self.rect.bottom = vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]

        # Движение по оси X
        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
            self.x_move = True
        elif keys[pygame.K_d]:
            self.rect.x += self.player_speed
            self.x_move = True
        else:
            self.x_move = False

        # Ограничение по оси X
        if self.rect.left <= vb.topleft_main_screen[0]:
            self.rect.left = vb.topleft_main_screen[0]
        elif self.rect.right >= vb.bottomright_main_screen[0]:
            self.rect.right = vb.bottomright_main_screen[0]

        self.angle = self.angle_towards_cursor(self.rect)

    def move_turn_mouse(self):
        '''Движение в сторону мыши'''
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.angle = self.angle_towards_cursor(self.rect)
                self.rect.x += self.player_speed * math.cos(math.radians(-self.angle))
                self.rect.y += self.player_speed * math.sin(math.radians(-self.angle))
            elif keys[pygame.K_s]:
                self.angle = self.angle_towards_cursor(self.rect)
                self.rect.x -= self.player_speed * math.cos(math.radians(-self.angle))
                self.rect.y -= self.player_speed * math.sin(math.radians(-self.angle))
            if keys[pygame.K_a]:
                self.angle = self.angle_towards_cursor(self.rect)
                self.rect.x -= self.player_speed * math.cos(math.radians(-self.angle + 90))
                self.rect.y -= self.player_speed * math.sin(math.radians(-self.angle + 90))
            elif keys[pygame.K_d]:
                self.angle = self.angle_towards_cursor(self.rect)
                self.rect.x += self.player_speed * math.cos(math.radians(-self.angle + 90))
                self.rect.y += self.player_speed * math.sin(math.radians(-self.angle + 90))

            # Ограничение по оси X
            if self.rect.left < vb.topleft_main_screen[0]:
                self.rect.left = vb.topleft_main_screen[0]

            if self.rect.right > vb.bottomright_main_screen[0]:
                self.rect.right = vb.bottomright_main_screen[0]

            # Ограничение по оси Y
            if self.rect.top < vb.topleft_main_screen[1]:
                self.rect.top = vb.topleft_main_screen[1]

            if self.rect.bottom > vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]:
                self.rect.bottom = vb.bottomright_main_screen[1] + vb.topleft_main_screen[1]


        self.image, self.rect = self.rotate_towards_cursor(self.original_image, self.rect)
        self.angle = self.angle_towards_cursor(self.rect)

    def move(self):
        '''
        Движение.
        В зависимости от настроек движения будет применять 1 из видов перемещения космического корабля игрока
        '''
        if self.player_ship_move_state == 0:
            self.move_straight()
        elif self.player_ship_move_state == 1:
            self.move_turn_straight()
        else:
            self.move_turn_mouse()

    def shoot(self, position):
        '''Стрельба'''
        keys = pygame.key.get_pressed()
        self.shoot_recharge_time -= 1
        revers_gun_bool = False
        if keys[pygame.K_SPACE] and self.shoot_recharge_time <= 0:
            self.shoot_recharge_time = self.shoot_basic_recharge_time
            self.bullet_group.add(bullet.Bullet(self.blast_data_tuple, self.bullet_image_tuple,
                                                self.asteroid_group, position,
                                  -self.angle, self.bullet_speed, self.player_damage))
            self.shoot_move = self.shoot_standart_move
            self.shoot_move_direction = -self.angle_towards_cursor(self.rect)
            
            revers_gun_bool = True
            
        if self.shoot_move > 0:
            self.rect.x -= self.shoot_move * math.cos(math.radians(self.shoot_move_direction))
            self.rect.y -= self.shoot_move * math.sin(math.radians(self.shoot_move_direction))
            
            self.shoot_move -= 1
        
        if revers_gun_bool:
            if self.revers_gun:
                self.revers_gun = not self.revers_gun
                return -85
            else:
                self.revers_gun = not self.revers_gun
                return 85

    def update_ship_has(self):
        '''Обновление прочности корабля игрока и его щита'''
        self.player_health_and_shield_background_group.update(self.rect, self.angle, None, False)
        self.player_health_group.update(self.rect, self.angle, self.health)
        self.player_shield_group.update(self.rect, self.angle, self.shield)

    def collision_asteroid(self):
        '''Столкновение с астероидами'''
        
        collision_count = 0
        
        for asteroid in self.asteroid_group:

            # Проверяем сталкиваются ли квадраты
            if self.rect.colliderect(asteroid.rect):

                # Создание оффсета
                offset = (asteroid.rect.topleft[0] - self.rect.left, asteroid.rect.topleft[1] - self.rect.top)
                
                # Проверка на столкновение масок
                if self.mask.overlap(asteroid.mask, offset):
                    
                    collision_count += 1 
                    
                    # Отключаем восстановление щита
                    self.shield_recovery = False

                    # Проверка на прочность щита выше 0
                    if self.shield > 0:
                        self.shield -= 1

                    # Если щит сломан отнимаем хитпоинты
                    elif self.health > 0:
                        self.health -= 1

                    # Если щит сломан и хитпоинты закончились уничтожаем корабль игрока
                    else:
                        self.ship_live = False
        
        if collision_count == 0:
            self.shield_recovery = True

    def repair_shield(self):
        '''Восстановление щита'''
        if self.shield_recovery:
            if self.shield + self.shield_repair_speed < self.basic_shield:
                self.shield += self.shield_repair_speed
            else:
                self.shield = self.basic_shield

    def load_controls(self):
        '''Загружает переменные для управления игрока'''
        
        controls = json_func.read(json_path.controls)
        
        self.control_move_up = controls['player_up_move']
        self.control_move_down = controls['player_down_move']
        self.control_move_left = controls['player_left_move']
        self.control_move_right = controls['player_right_move']
        self.control_shoot = controls['player_shoot']
