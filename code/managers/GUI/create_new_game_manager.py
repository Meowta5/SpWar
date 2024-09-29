
from random import choice

from pygame import Rect
import pygame
from pygame_gui.elements import UIDropDownMenu, UIButton, UITextEntryLine, UILabel
from pygame_gui.core import ObjectID
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED, UI_TEXT_ENTRY_CHANGED

from code.function import ratio_value
import code.function as func
import code.variable as vb
import code.path.image_path as image_path
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager
from code.object.static_object import StaticObject


class CreateNewGameManager(InheritanceGUIManager):
    def __init__(self, ui_manager, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.ui_manager = ui_manager
        
        self.gui_dict['create_new_game'] = []
        self.ship_group = pygame.sprite.GroupSingle()
        
        self.game_name = ''
        self.done_but_block = False

        self.select_ship = 'random'
        self.select_difficulty = 'random'
        self.game_name = ''
        
        self._create_buttons()
        self._create_drop_menu()
        self._create_labels()
        self._create_text_entry_line()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        self.return_but.set_text(word.return_)
        self.done_but.set_text(word.done)
        
        self.difficulty_label.set_text(word.difficulty)
        self.ship_label.set_text(word.ship)
        self.there_is_name_label.set_text(word.there_is_name)
        
        self._replacement_drop_menu()
        self._replacement_text_entry_line()

    def check_event(self, event):
        '''Проверка событий GUI'''
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.return_but:
                self._reset_data()
                return 'switch load_menu'
            elif event.ui_element == self.done_but and not self.done_but_block:
                self._create_new_game_func()
                game_name = self.game_name
                self._reset_data()
                return ('switch start_menu', game_name)
        elif event.type == UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.difficulty_menu:
                self.select_difficulty = event.text
            elif event.ui_element == self.ship_menu:
                if event.text == word.damnium:
                    self.select_ship = 'damnium'
                elif event.text == word.libra:
                    self.select_ship = 'libra'
                elif event.text == word.celeritas:
                    self.select_ship = 'celeritas'
                elif event.text == word.versi:
                    self.select_ship = 'versi'
                elif event.text == word.random:
                    self.select_ship = 'random'
        elif event.type == UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.name_line:
                if event.text in vb.game_saves.keys():
                    self.there_is_name_label.show()
                    self.done_but_block = True
                else:
                    self.there_is_name_label.hide()
                    self.done_but_block = False
                self.game_name = event.text

    def update_and_draw(self, need_kill, screen, screen_rect):
        '''Обновляет, рисует, статичный корабль'''
        self.ship_group.update(need_kill, screen_rect)
        self.ship_group.draw(screen)

    def start(self):
        '''Инициализация всего необходимого для работы менеджера'''

    def _reset_data(self):
        '''Очищает все введенные данные'''
        self.name_line.clear()
        self._replacement_drop_menu()
        self.select_ship = 'random'
        self.select_difficulty = 'random'
        self.game_name = ''

    def _create_new_game_func(self):
        new_game = {
                    "damnium_buy": False,
                    "versi_buy": False,
                    "celeritas_buy": False,
                    "libra_buy": False,
                    "start_ship": "",
                    "damnium_param": {
                        "speed": 10,
                        "damage": 25,
                        "shield_repair_speed": 1,
                        "shield": 100,
                        "health": 100,
                        "recharge": 45,
                        "shoot_move": 10
                    },
                    "versi_param": {
                        "speed": 10,
                        "damage": 25,
                        "shield_repair_speed": 1,
                        "shield": 100,
                        "health": 100,
                        "recharge": 45,
                        "shoot_move": 10
                    },
                    "celeritas_param": {
                        "speed": 10,
                        "damage": 25,
                        "shield_repair_speed": 1,
                        "shield": 100,
                        "health": 100,
                        "recharge": 45,
                        "shoot_move": 10
                    },
                    "libra_param": {
                        "speed": 10,
                        "damage": 25,
                        "shield_repair_speed": 1,
                        "shield": 100,
                        "health": 100,
                        "recharge": 45,
                        "shoot_move": 10
                    },
                    "record": 0,
                    "money": 0,
                    "rupiy": 0,
                    "elerius": 0,
                    "duranty": 0,
                    "astrius": 0,
                    "difficulty": ""
        }
     
        if self.select_ship == 'random':
            ship = choice(('damnium', 'celeritas', 'versi', 'libra'))
        else:
            ship = self.select_ship
        if self.select_difficulty == 'random':
            difficulty = choice(('easy', 'medium', 'hard'))
        else:
            difficulty = self.select_difficulty

        new_game[f'{ship}_buy'] = True
        new_game['start_ship'] = ship
        new_game['difficulty'] = difficulty

        vb.game_saves[self.game_name] = new_game
        json_func.write(vb.game_saves, json_path.game_saves)
        vb.load_game_saves_json()
        self.game_name = self.game_name

    def _create_buttons(self):
        '''Создание кнопок'''
        self.return_but = UIButton(
            relative_rect=Rect((ratio_value(100), ratio_value(525)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.return_, manager=self.ui_manager
        )
        self.done_but = UIButton(
            relative_rect=Rect((ratio_value(900), ratio_value(525)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.done, manager=self.ui_manager
        )
        self.gui_dict['create_new_game'].append(self.return_but)
        self.gui_dict['create_new_game'].append(self.done_but)

    def _create_drop_menu(self):
        '''Создаение выдающих меню'''
        difficulty_tuple = (word.easy, word.medium, word.hard, word.random)
        self.difficulty_menu = UIDropDownMenu(
            relative_rect=Rect((ratio_value(900), ratio_value(50)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=difficulty_tuple,
            starting_option=difficulty_tuple[3], manager=self.ui_manager
        )
        ship_tuple = (word.damnium, word.libra, word.celeritas, word.versi, word.random)
        self.ship_menu = UIDropDownMenu(
            relative_rect=Rect((ratio_value(900), ratio_value(125)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=ship_tuple,
            starting_option=ship_tuple[4], manager=self.ui_manager
        )
        
        self.gui_dict['create_new_game'].append(self.difficulty_menu)
        self.gui_dict['create_new_game'].append(self.ship_menu)

    def _create_labels(self):
        '''Создание надписей'''
        self.difficulty_label = UILabel(
            relative_rect=Rect((ratio_value(675), ratio_value(50)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.difficulty, manager=self.ui_manager
        )
        self.ship_label = UILabel(
            relative_rect=Rect((ratio_value(675), ratio_value(125)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.ship, manager=self.ui_manager
        )
        self.there_is_name_label = UILabel(
            relative_rect=Rect((ratio_value(100), ratio_value(110)),
                                      (ratio_value(500), ratio_value(50))),
            text=word.there_is_name, manager=self.ui_manager,
            object_id=ObjectID(class_id='#error_label')
        )
        
        self.gui_dict['create_new_game'].append(self.difficulty_label)
        self.gui_dict['create_new_game'].append(self.ship_label)
        self.gui_dict['create_new_game'].append(self.there_is_name_label)

    def _create_text_entry_line(self):
        '''Создание строк ввода текста'''
        self.name_line = UITextEntryLine(
            relative_rect=Rect(ratio_value(100), ratio_value(50),
                               ratio_value(500), ratio_value(50)),
            placeholder_text=word.input_name_game,
            manager=self.ui_manager
        )
        self.gui_dict['create_new_game'].append(self.name_line)

    def _replacement_drop_menu(self):
        '''Удаляет прошлое и создает новые меню выпадающие вниз'''
        self.gui_dict['create_new_game'].remove(self.difficulty_menu)
        self.difficulty_menu.kill()
        
        self.gui_dict['create_new_game'].remove(self.ship_menu)
        self.ship_menu.kill()
        
        self._create_drop_menu()

    def _replacement_text_entry_line(self):
        '''Удаляет и создает новую линию ввода текста'''
        self.gui_dict['create_new_game'].remove(self.name_line)
        self.name_line.kill()
        self._create_text_entry_line()

    def _create_damnium(self):
        ship = StaticObject(
            func.load_gif(image_path.damnium_ship_path, vb.background_size_coeff * 0.5),
            (ratio_value(1000), ratio_value(300)), 0.55
        )
        self.ship_group.add(ship)

    def _create_libra(self):
        ship = StaticObject(
            func.load_gif(image_path.libra_ship_path, vb.background_size_coeff * 0.5),
            (ratio_value(1000), ratio_value(300)), 0.55
        )
        self.ship_group.add(ship)

    def _create_celeritas(self):
        ship = StaticObject(
            func.load_gif(image_path.celeritas_ship_path, vb.background_size_coeff * 0.25),
            (ratio_value(1000), ratio_value(300)), 0.55
        )
        self.ship_group.add(ship)

    def _create_versi(self):
        ship = StaticObject(
            func.load_gif(image_path.versi_ship_path, vb.background_size_coeff * 0.5),
            (ratio_value(1000), ratio_value(300)), 0.55
        )
        self.ship_group.add(ship)
