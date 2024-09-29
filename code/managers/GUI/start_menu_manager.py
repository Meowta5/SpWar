
import pygame
from pygame import Rect
from pygame_gui.elements import UILabel, UIButton
from pygame_gui.core import ObjectID
from pygame_gui import UI_BUTTON_PRESSED

from code.function import ratio_value
import code.variable as vb
import code.function as func
import code.path.image_path as image_path
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager
from code.object.static_object import StaticObject


class StartMenuManager(InheritanceGUIManager):
    def __init__(self, ui_manager, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.ui_manager = ui_manager

        self.gui_dict['start_menu'] = []

        self.ship_index = 0
        self.move_ship = False
        self.move_two_ship = False
        self.now_ship = None
        self.now_ship_speed = None
        self.new_ship = None
        self.new_ship_speed = None
        self.ship_swtich_timer = 0

        self._create_buttons()
        self._create_labels()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        self.start_but.set_text(word.start)
        self.switch_load_menu_but.set_text(word.go_to_load_menu)
        self.parameters_but.set_text(word.parameters)

        self.ship_label.set_text(
            (word.damnium, word.versi, word.celeritas, word.libra)[self.ship_index]
        )

    def update_and_draw(self, screen, need_kill):
        self._move_logic()
        for i in self.ship_data_dict.values():
            i[0].update(need_kill, self.screen_rect)
            i[0].draw(screen)

    def check_event(self, event):
        '''Проверка событий GUI'''
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.start_but:
                print('START')
            elif event.ui_element == self.switch_load_menu_but:
                return 'switch load_menu'
            elif event.ui_element == self.parameters_but:
                return ('switch start_menu', self.now_ship)
            elif event.ui_element == self.right_ship_but:
                self._change_ship('right')
            elif event.ui_element == self.left_ship_but:
                self._change_ship('left')

    def restart(self, screen_rect):
        '''Инициализация всего необходимого для работы менеджера'''
        self.screen_rect = screen_rect
        self.ship_label.set_text(vb.game_save['start_ship'])

        # Наличие кораблей
        vb.damnium_buy = vb.game_save['damnium_buy']
        vb.versi_buy = vb.game_save['versi_buy']
        vb.celeritas_buy = vb.game_save['celeritas_buy']
        vb.libra_buy = vb.game_save['libra_buy']
        
        # Их характеристики
        vb.damnium_param = vb.game_save['damnium_param']
        vb.versi_param = vb.game_save['versi_param']
        vb.celeritas_param = vb.game_save['celeritas_param']
        vb.libra_param = vb.game_save['libra_param']
        
        # Кол-во ресурсов
        vb.record = vb.game_save['record']
        vb.money = vb.game_save['money']
        vb.rupiy = vb.game_save['rupiy']
        vb.elerius = vb.game_save['elerius']
        vb.duranty = vb.game_save['duranty']
        vb.astrius = vb.game_save['astrius']

        self._reset_data()
        print('УСПЕШНЫЙ РЕСТАРТ')
        self.move_ship = True
        self.x_pos = ratio_value(600)

    def data_update(self):
        '''Обновление данных менеджера'''
        self.ship_data_dict = {
            'damnium': [pygame.sprite.GroupSingle(), False],
            'celeritas': [pygame.sprite.GroupSingle(), False],
            'versi': [pygame.sprite.GroupSingle(), False],
            'libra': [pygame.sprite.GroupSingle(), False],
        }
        self.ship_data_dict['damnium'][0].add(
            StaticObject(
                func.load_gif(image_path.damnium_ship_path,
                              vb.background_size_coeff * 0.5),
                              (ratio_value(-250), ratio_value(300)), 0.55
            )
        )
        self.ship_data_dict['versi'][0].add(
            StaticObject(
                func.load_gif(image_path.versi_ship_path,
                              vb.background_size_coeff * 0.5),
                              (ratio_value(-250), ratio_value(300)), 0.55
            )
        )
        self.ship_data_dict['celeritas'][0].add(
            StaticObject(
                func.load_gif(image_path.celeritas_ship_path,
                              vb.background_size_coeff * 0.25),
                              (ratio_value(-250), ratio_value(300)), 0.55
            )
        )
        self.ship_data_dict['libra'][0].add(
            StaticObject(
                func.load_gif(image_path.libra_ship_path,
                              vb.background_size_coeff * 0.5),
                              (ratio_value(-250), ratio_value(300)), 0.55
            )
        )

    def _reset_data(self):
        self._define_start_ship()
        self.ship_label.set_text(
            (word.damnium, word.versi, word.celeritas, word.libra)[self.ship_index]
        )
        for i in self.ship_data_dict.values():
            i[0].sprite.move((ratio_value(-250), ratio_value(300)))

    def _create_buttons(self):
        '''Создание кнопок'''
        self.start_but = UIButton(
            relative_rect=Rect((ratio_value(400), ratio_value(25)),
                                      (ratio_value(400), ratio_value(50))),
            text=word.start, manager=self.ui_manager
        )
        self.switch_load_menu_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(100), ratio_value(525)),
                                      (ratio_value(225), ratio_value(50))),
            text=word.go_to_load_menu, manager=self.ui_manager
        )
        self.parameters_but = UIButton(
            relative_rect=Rect((ratio_value(400), ratio_value(530)),
                                      (ratio_value(400), ratio_value(50))),
            text=word.parameters, manager=self.ui_manager, object_id=ObjectID(
                class_id='#rect_button_two_bottom'
            )
        )
        self.left_ship_but = UIButton(
            relative_rect=Rect((ratio_value(400), ratio_value(479)),
                                      (ratio_value(50), ratio_value(52))),
            text='<--', manager=self.ui_manager, object_id=ObjectID(
                class_id='#rect_button_topleft'
            )
        )
        self.right_ship_but = UIButton(
            relative_rect=Rect((ratio_value(750), ratio_value(479)),
                                      (ratio_value(50), ratio_value(52))),
            text='-->', manager=self.ui_manager, object_id=ObjectID(
                class_id='#rect_button_topright'
            )
        )

        self.gui_dict['start_menu'].append(self.start_but)
        self.gui_dict['start_menu'].append(self.switch_load_menu_but)
        self.gui_dict['start_menu'].append(self.parameters_but)
        self.gui_dict['start_menu'].append(self.left_ship_but)
        self.gui_dict['start_menu'].append(self.right_ship_but)

    def _create_labels(self):
        '''Создание надписей'''
        self.ship_label = UILabel(
            relative_rect=Rect((ratio_value(450), ratio_value(480)),
                                      (ratio_value(300), ratio_value(50))),
            text='None', manager=self.ui_manager
        )
        self.gui_dict['start_menu'].append(self.ship_label)

    def _define_start_ship(self):
        ship = vb.game_save['start_ship']
        self.ship_data_dict[ship][1] = True
        self.now_ship_speed = vb.game_save[f'{ship}_param']['speed']
        self.now_ship = ship

    def _move_logic(self):
        data = self._set_move_ship()
        self.ship_swtich_timer -= 1
        timer = self.ship_swtich_timer <= 0
        if data is True and timer:
            self.move_two_ship = not self.move_two_ship
        if (self.move_two_ship
            and not self.new_ship is None
            and not self.new_ship_speed is None
            and timer):

            for el in self.ship_data_dict.values():
                el[0].sprite.move((ratio_value(-250), ratio_value(300)))

            self.now_ship = self.new_ship
            self.now_ship_speed = self.new_ship_speed

            self.x_pos = ratio_value(600)

            self.new_ship = None
            self.new_ship_speed = None

    def _set_move_ship(self):
        '''.'''
        if self.move_ship:
            print('MOVE SHIP')
            ship = self.ship_data_dict[self.now_ship][0].sprite
            rect = ship.get_rect()
            rect.x += self.now_ship_speed

            if ((rect.x < self.x_pos and self.now_ship_speed < 0)
                or (rect.x > self.x_pos and self.now_ship_speed > 0)):

                rect.x = self.x_pos
                ship.set_rect(rect)
                print('MOVE SHIP RETURN TRUE')
                return True
            else:
                ship.set_rect(rect)

    def _change_ship(self, side):
        if side == 'left':
            if self.ship_index == 0:
                self.ship_index = 3
            else:
                self.ship_index -= 1
        elif side == 'right':
            if self.ship_index == 3:
                self.ship_index = 0
            else:
                self.ship_index += 1
        
        #if self.move_ship:
        #    self.now_ship = self.new_ship
        #    self.now_ship_speed = self.new_ship_speed

        self.new_ship = ('damnium', 'versi', 'celeritas', 'libra')[self.ship_index]
        self.new_ship_speed = vb.game_save[f'{self.new_ship}_param']['speed']

        self.ship_label.set_text(
            (word.damnium, word.versi, word.celeritas, word.libra)[self.ship_index]
        )
        self.x_pos = ratio_value(1650)
        self.ship_swtich_timer = 120
        self.move_ship = True
