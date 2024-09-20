
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

        self.move_ship = False
        self.now_ship = None
        self.new_ship = None
        self.now_ship_speed = 0
        self.new_ship_speed = 0
        self.buy_ships = []
        self.ship_index = 0

        self._create_buttons()
        self._create_labels()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''

    def update_and_draw(self, screen, need_kill):
        if self.start_ship:
            self._start_ship_move(ratio_value(600))

        self._ship_move_logic()

        for i in self.ship_data_dict.values():
            i[0].update(need_kill, self.screen_rect)
            i[0].draw(screen)

    def check_event(self, event):
        '''Проверка событий GUI'''
        if not self.move_ship and not self.start_ship:
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.start_but:
                    print('START')
                elif event.ui_element == self.switch_load_menu_but:
                    return 'switch load_menu'
                elif event.ui_element == self.parameters_but:
                    print('PARAMETERS')
                elif event.ui_element == self.right_ship_but:
                    self._change_ship('right')
                elif event.ui_element == self.left_ship_but:
                    self._change_ship('left')

    def start(self, game_save, screen_rect):
        '''Инициализация всего необходимого для работы менеджера'''
        self.game_save = game_save
        self.screen_rect = screen_rect
        self.ship_label.set_text(game_save['start_ship'])

        # Наличие кораблей
        vb.damnium_buy = game_save['damnium_buy']
        vb.versi_buy = game_save['versi_buy']
        vb.celeritas_buy = game_save['celeritas_buy']
        vb.libra_buy = game_save['libra_buy']
        
        # Их характеристики
        vb.damnium_param = game_save['damnium_param']
        vb.versi_param = game_save['versi_param']
        vb.celeritas_param = game_save['celeritas_param']
        vb.libra_param = game_save['libra_param']
        
        # Кол-во ресурсов
        vb.record = game_save['record']
        vb.money = game_save['money']
        vb.rupiy = game_save['rupiy']
        vb.elerius = game_save['elerius']
        vb.duranty = game_save['duranty']
        vb.astrius = game_save['astrius']

        self.start_ship = True
        self._reset_data()

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
        self._set_ships_list()
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

    def _replacement_drop_menu(self):
        '''Удаляет прошлое и создает новые меню выпадающие вниз'''

    def _set_ships_list(self):
        self.buy_ships.clear()
        if self.game_save['damnium_buy']:
            self.ship = word.damnium
            self.ship_index = 0
        if self.game_save['versi_buy']:
            self.ship = word.versi
            self.ship_index = 1
        if self.game_save['celeritas_buy']:
            self.ship = word.celeritas
            self.ship_index = 2
        if self.game_save['libra_buy']:
            self.ship = word.libra
            self.ship_index = 3
    
    def _ship_move_logic(self):
        if self.move_ship:
            if self.ship_data_dict[self.now_ship][0].sprite.get_rect().colliderect(
                self.screen_rect
            ):
                rect = self.ship_data_dict[self.now_ship][0].sprite.get_rect()
                self.ship_data_dict[self.now_ship][0].sprite.move(
                    (rect.center[0] + self.now_ship_speed, rect.center[1])
                )
            else:
                rect = self.ship_data_dict[self.new_ship][0].sprite.get_rect()
                new_position = rect.center[0] + self.new_ship_speed, rect.center[1]
                if new_position[0] < ratio_value(600):
                    self.ship_data_dict[self.new_ship][0].sprite.move(new_position)
                else:
                    self.ship_data_dict[self.now_ship][0].sprite.move(
                        (ratio_value(-250), ratio_value(300))
                    )
                    self.now_ship = self.new_ship
                    self.now_ship_speed = self.new_ship_speed
                    self.new_ship = None
                    self.new_ship_speed = 0
                    self.move_ship = False

    def _start_ship_move(self, new_x):
        if self.start_ship:
            if (self.ship_data_dict[self.now_ship][0].sprite.get_rect()[0]
                + self.now_ship_speed < new_x):
                rect = self.ship_data_dict[self.now_ship][0].sprite.get_rect()
                self.ship_data_dict[self.now_ship][0].sprite.move(
                        (rect.center[0] + self.now_ship_speed, rect.center[1])
                )
            elif self.now_ship_speed > new_x:
                rect = self.ship_data_dict[self.now_ship][0].sprite.get_rect()
                self.ship_data_dict[self.now_ship][0].sprite.move((new_x, rect.center[1]))
            else:
                self.start_ship = False

    def _define_start_ship(self):
        ship = self.game_save['start_ship']
        self.ship_data_dict[ship][1] = True
        self.now_ship_speed = self.game_save[f'{ship}_param']['speed']
        self.now_ship = ship

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
        self.new_ship = ('damnium', 'versi', 'celeritas', 'libra')[self.ship_index]
        self.new_ship_speed = self.game_save[
            f'{('damnium', 'versi', 'celeritas', 'libra')[self.ship_index]}_param']['speed'
        ]
        self.ship_label.set_text(
            (word.damnium, word.versi, word.celeritas, word.libra)[self.ship_index]
        )
        self.move_ship = True
