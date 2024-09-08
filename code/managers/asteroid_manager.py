
from random import randint, choice

import pygame

import code.function as function
import code.variable as vb
import code.path.image_path as image_path
from code.object import asteroid


class AsteroidManager:
    def __init__(self, clock):
        # Астероиды
        self.asteroid_group = pygame.sprite.Group()
        self.asteroid_image_list = []
        
        # Маленький
        self.small_parameters = [
            (4, 7), # Границы прочности 0
            (4, 9), # Границы скорости вращения 1
            (4, 8)  # Границы скорости перемещения 2
        ]
        
        # Средний
        self.medium_parameters = [
            (25, 45), # Границы прочности 0
            (3, 6), # Границы скорости вращения 1
            (3, 5)  # Границы скорости перемещения 2
        ]
        
        # Большой
        self.big_parameters = [
            (65, 85), # Границы прочности 0
            (2, 5), # Границы скорости вращения 1
            (1, 3)  # Границы скорости перемещения 2
        ]
        
        # FPS
        self.fps_list = [0 for _ in range(30)]
        self.clock = clock
        
        # Генератор
        self.generator_point = 3600
        self.generator_point_add = 3
        
        self.gpa_up = 0
        self.need_up_gpa = 1
        self.need_up_gpa_tuple = (125, 250, 375, 500, 625, 750, 875,
                                  1000, 1125, 1250, 1375, 1500, 1625, 1750, 1875,
                                  2000, 2125, 2250, 2375, 2500, 2625, 2750, 2875,
                                  3000, 3125, 3250, 3375, 3500, 3625, 3750, 3875,
                                  4000, 4125, 4250, 4375, 4500, 4625, 4750, 4875,
                                  5000, 5125, 5250, 5375, 5500, 5625, 5750, 5875,
                                  6000, 6125, 6250, 6375, 6500, 6625, 6750, 6875,
                                  7000, 7125, 7250, 7375, 7500, 7625, 7750, 7875,
                                  8000, 8125, 8250, 8375, 8500, 8625, 8750, 8875,
                                  9000, 9125, 9250, 9375, 9500, 9625, 9750, 9875, 10000)
        self.gpa_tuple_ind = 0
        
        self.max_asteroid_len = 21
        self.max_asteroid_len_add = 6

        # Взрыв
        self.blast_manager = None

    def define_medium_fps(self):
        '''Рассчитывает средний ФПС'''
        self.fps_list.pop(0)
        self.fps_list.append(self.clock.get_fps())
        
        return sum(self.fps_list) / len(self.fps_list)
        
    def import_asteroid_image(self):
        '''Импорт изображений астероидов'''
        
        image_list = []
        for i in image_path.asteroid_path_one:
            image_list.append(function.load_image(i, 1))
        
        self.asteroid_image_list += image_list
        
    def define_size_asteroid(self, type: int):
        '''Расчет размера астероида
        0 Маленький
        1 Средний
        2 Большой
        '''
        size = vb.background_size_coeff
        if type == 0: # Маленький
            size *= float(f'0.0{randint(3, 7)}{randint(5, 9)}{randint(5, 9)}')
        elif type == 1: # Средний
            size *= float(f'0.1{randint(4, 7)}{randint(4, 9)}')
        elif type == 2: # Большой
            size *= float(f'0.2{randint(5, 7)}{randint(1, 5)}')
        
        else:
            raise ValueError('')

        return size
  
    def create_param_asteroid(self, asteroid_type, size: float, angle_speed: float,
                              asteroid_speed: float, health: float):
        '''Создание астероида'''
        created_asteroid = asteroid.Asteroid(
            (self.blast_manager, asteroid_type, size),
            pygame.transform.rotozoom(choice(self.asteroid_image_list), 0, size),
            angle_speed, asteroid_speed, health)
        
        asteroid_rect = created_asteroid.return_rect()
        x_pos = randint(vb.bottomright_main_screen[0] * 1.25 + asteroid_rect.width,
                        vb.bottomright_main_screen[0] * 1.75)

        asteroid_height_size = asteroid_rect.height / 2
        y_pos = randint(int(vb.topleft_main_screen[1] + asteroid_height_size),
                        int(vb.bottomright_main_screen[1] - asteroid_height_size))
        
        created_asteroid.teleport_position((x_pos, y_pos))
        self.asteroid_group.add(created_asteroid)
    
    def create_small_asteroid(self):
        '''Создает маленький астероид'''
        size = self.define_size_asteroid(0)
        
        health = randint(*map(int, self.small_parameters[0]))
        angle_speed = randint(*map(int, self.small_parameters[1]))
        asteroid_speed = function.ratio_value(randint(*map(int, self.small_parameters[2])))
        
        self.create_param_asteroid('small', size, angle_speed, asteroid_speed, health)

    def create_medium_asteroid(self):
        '''Создает средний астероид'''
        size = self.define_size_asteroid(1)
        
        health = randint(*map(int, self.medium_parameters[0]))
        angle_speed = randint(*map(int, self.medium_parameters[1]))
        asteroid_speed = function.ratio_value(randint(*map(int, self.medium_parameters[2])))
        
        self.create_param_asteroid('medium', size, angle_speed, asteroid_speed, health)
       
    def create_big_asteroid(self):
        '''Создает большой астероид'''
        size = self.define_size_asteroid(2)
        
        health = randint(*map(int, self.big_parameters[0]))
        angle_speed = randint(*map(int, self.big_parameters[1]))
        asteroid_speed = function.ratio_value(randint(*map(int, self.big_parameters[2])))
        
        self.create_param_asteroid('big', size, angle_speed, asteroid_speed, health)

    def small_asteroid_params_up(self):
        '''Увелечение параметров маленьких астероидов'''

        self.small_parameters[0] = (
            int(self.small_parameters[0][0] * 1.0185),
            int(self.small_parameters[0][1] * 1.0185)
        )
        self.small_parameters[1] = (
            (self.small_parameters[1][0] * 1.003),
            (self.small_parameters[1][1] * 1.003)
        )
        self.small_parameters[2] = (
            (self.small_parameters[2][0] * 1.0125),
            (self.small_parameters[2][1] * 1.0125)
        )

    def medium_asteroid_params_up(self):
        '''Увелечение параметров средних астероидов'''

        self.medium_parameters[0] = (
            int(self.medium_parameters[0][0] * 1.02),
            int(self.medium_parameters[0][1] )
        )
        self.medium_parameters[1] = (
            (self.medium_parameters[1][0] * 1.00399),
            (self.medium_parameters[1][1] * 1.00399)
        )
        self.medium_parameters[2] = (
            (self.medium_parameters[2][0] * 1.00785),
            (self.medium_parameters[2][1] * 1.00785)
        )

    def big_asteroid_params_up(self):
        '''Увелечение параметров больших астероидов'''

        self.big_parameters[0] = (
            int(self.big_parameters[0][0] * 1.0235),
            int(self.big_parameters[0][1] * 1.0235)
        )
        self.big_parameters[1] = (
            (self.big_parameters[1][0] * 1.00314),
            (self.big_parameters[1][1] * 1.00314)
        )
        self.big_parameters[2] = (
            (self.big_parameters[2][0] * 1.00675),
            (self.big_parameters[2][1] * 1.00675)
        )

    def asteroid_params_up(self):
        '''Увелечение параметров астероидов'''
        self.small_asteroid_params_up()
        self.medium_asteroid_params_up()
        self.big_asteroid_params_up()

    def asteroid_generator(self):
        '''Создает астероиды'''
        if len(self.asteroid_group) < self.max_asteroid_len and self.define_medium_fps() > 29:
            self.generator_point += self.generator_point_add
            if self.generator_point > 300:

                while self.generator_point >= 30:
                    ast_type = choice(('small', 'medium', 'big'))
                    if ast_type == 'small' and self.generator_point >= 30:
                        self.generator_point -= 30
                        self.create_small_asteroid()
                    elif ast_type == 'medium' and self.generator_point >= 165:
                        self.generator_point -= 165
                        self.create_medium_asteroid()
                    elif ast_type == 'big' and self.generator_point >= 300:
                        self.generator_point -= 300
                        self.create_big_asteroid()
                        
                if self.gpa_up == self.need_up_gpa:
                    self.gpa_up = 0
                    if self.gpa_tuple_ind < 78:
                        self.gpa_tuple_ind += 1
                        self.max_asteroid_len_add += 3
                        self.max_asteroid_len += self.max_asteroid_len_add
                        self.need_up_gpa = self.need_up_gpa_tuple[self.gpa_tuple_ind]
                        self.asteroid_params_up()
                else:
                    self.gpa_up += 1
                self.generator_point_add += 0.05

    def update(self, sea_area_rect):
        '''Обновление группы астероидов'''
        self.asteroid_group.update(sea_area_rect)
    
    def draw(self, screen):
        '''Отрисовка группы астероидов'''
        self.asteroid_group.draw(screen)

    def start(self, blast_manager):
        '''Инициализая и импорт всего необходимого для нормальной работы менеджера'''
        self.blast_manager = blast_manager
        self.import_asteroid_image()
