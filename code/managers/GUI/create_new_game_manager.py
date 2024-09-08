
from pygame import Rect
import pygame
from pygame_gui.elements import UIDropDownMenu, UIButton, UITextEntryLine, UILabel
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED, UI_TEXT_ENTRY_CHANGED

from code.function import ratio_value
import code.function as func
import code.variable as vb
import code.path.image_path as image_path
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
                self.name_line.clear()
                self._replacement_drop_menu()
                return 'switch load_menu'
            elif event.ui_element == self.done_but and not self.done_but_block:
                return ''
        elif event.type == UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.difficulty_menu:
                ...#word.easy, word.medium, word.hard, word.random
            elif event.ui_element == self.ship_menu:
                if event.text == word.damnium:
                    self._create_damnium()
                elif event.text == word.libra:
                    self._create_libra()
                elif event.text == word.celeritas:
                    self._create_celeritas()
                elif event.text == word.versi:
                    self._create_versi()
                elif event.text == word.random:
                    self.ship_group.empty()
        elif event.type == UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.name_line:
                if event.text in vb.game_saves.keys():
                    self.there_is_name_label.show()
                    self.done_but_block = True
                else:
                    self.there_is_name_label.hide()
                    self.done_but_block = False
                self.game_name = event.text

    def check_static_ship(self, need_kill, screen):
        '''Обновляет, рисует, статичный корабль'''
        self.ship_group.update(need_kill)
        self.ship_group.draw(screen)

    def start(self):
        '''Инициализация всего необходимого для работы менеджера'''

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
            text=word.there_is_name, manager=self.ui_manager
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
            (1000, 300), 0.55
        )
        self.ship_group.add(ship)

    def _create_libra(self):
        ship = StaticObject(
            func.load_gif(image_path.libra_ship_path, vb.background_size_coeff * 0.5),
            (1000, 300), 0.55
        )
        self.ship_group.add(ship)

    def _create_celeritas(self):
        ship = StaticObject(
            func.load_gif(image_path.celeritas_ship_path, vb.background_size_coeff * 0.25),
            (1000, 300), 0.55
        )
        self.ship_group.add(ship)

    def _create_versi(self):
        ship = StaticObject(
            func.load_gif(image_path.versi_ship_path, vb.background_size_coeff * 0.5),
            (1000, 300), 0.55
        )
        self.ship_group.add(ship)
