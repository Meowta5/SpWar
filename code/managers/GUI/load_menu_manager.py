
from sys import exit

import pygame
from pygame_gui.elements import UIWindow, UISelectionList, UIButton, UILabel
from pygame_gui import UI_BUTTON_PRESSED, UI_WINDOW_CLOSE

from code.function import ratio_value
import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager


class LoadMenuManager(InheritanceGUIManager):
    def __init__(self, ui_manager, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.ui_manager = ui_manager
        
        self.gui_dict['load_menu'] = []
        self.window_activ = False
        self.delete_game_key = ''
        
        self._create_buttons()
        self._create_selection_list()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        self.create_new_game_but.set_text(word.new_game)
        self.load_game_but.set_text(word.load_game)
        self.delete_game_but.set_text(word.delete_game)
        self.settings_but.set_text(word.settings)
        self.exit_but.set_text(word.exit)

    def check_event(self, event):
        '''Проверка событий GUI'''
        if not self.window_activ:
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.create_new_game_but:
                    return 'switch create_new_game'
                elif event.ui_element == self.load_game_but:
                    self._load_game_func()
                    return 'switch select_ship'
                elif event.ui_element == self.delete_game_but:
                    self._delete_game_func()
                elif event.ui_element == self.settings_but:
                    return 'switch settings'
        else:
            if event.type == UI_WINDOW_CLOSE:
                if event.ui_element == self.yn_window:
                    self.window_activ = False
            elif event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.yes_yn_window_but:
                    self.window_activ = False
                    self._delete_game()
                    self.yn_window.kill()
                elif event.ui_element == self.no_yn_window_but:
                    self.window_activ = False
                    self._delete_game()
                    self.yn_window.kill()
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.exit_but:
                self._exit_func()

    def start(self, gui_manager):
        '''Инициализация всего необходимого для работы менеджера'''
        self.gui_manager = gui_manager

    def _create_buttons(self):
        '''Создание кнопок'''
        self.create_new_game_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(100)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.new_game, manager=self.ui_manager
        )
        self.load_game_but = UIButton(
                relative_rect=pygame.Rect((ratio_value(75), ratio_value(160)),
                                        (ratio_value(200), ratio_value(50))),
                text=word.load_game, manager=self.ui_manager
        )
        self.delete_game_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(220)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.delete_game, manager=self.ui_manager
        )
        self.settings_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(280)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.settings, manager=self.ui_manager
        )
        self.exit_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(340)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.exit, manager=self.ui_manager
        )
        self.gui_dict['load_menu'].append(self.create_new_game_but)
        self.gui_dict['load_menu'].append(self.load_game_but)
        self.gui_dict['load_menu'].append(self.delete_game_but)
        self.gui_dict['load_menu'].append(self.settings_but)
        self.gui_dict['load_menu'].append(self.exit_but)

    def _create_selection_list(self):
        '''Создание меню выбора игры'''
        self.game_selection_list = UISelectionList(
            relative_rect=pygame.Rect((ratio_value(300), ratio_value(75)),
                                      (ratio_value(800), ratio_value(400))),
            item_list=[i for i in vb.game_saves.keys()],
            manager=self.ui_manager
        )
        self.gui_dict['load_menu'].append(self.game_selection_list)

    def _load_game_func(self):
        '''Загружает игру по ключу'''
        game_key = self.game_selection_list.get_single_selection()
        
        if game_key is not None:
            game_saves_dict = json_func.read(json_path.game_saves)
            game_dict = game_saves_dict[game_key]
            
            # Наличие кораблей
            vb.damnium_buy = game_dict['damnium_buy']
            vb.versi_buy = game_dict['versi_buy']
            vb.celeritas_buy = game_dict['celeritas_buy']
            vb.libra_buy = game_dict['libra_buy']
            
            # Их характеристики
            vb.damnium_param = game_dict['damnium_param']
            vb.versi_param = game_dict['versi_param']
            vb.celeritas_param = game_dict['celeritas_param']
            vb.libra_param = game_dict['libra_param']
            
            # Кол-во ресурсов
            vb.record = game_dict['record']
            vb.money = game_dict['money']
            vb.rupiy = game_dict['rupiy']
            vb.elerius = game_dict['elerius']
            vb.duranty = game_dict['duranty']
            vb.astrius = game_dict['astrius']

    def _delete_game_func(self):
        '''Функция для кнопки "Удалить игру"'''
        self.delete_game_key = self.game_selection_list.get_single_selection()
        if self.delete_game_key is not None:
            self.window_activ = True
            self.yn_window = UIWindow(
                pygame.Rect(ratio_value(450),
                            ratio_value(225)
                            ,ratio_value(300),
                            ratio_value(150)),
                manager=self.ui_manager, window_display_title=''
            )
            self.yes_yn_window_but = UIButton(
                relative_rect=pygame.Rect(ratio_value(20),
                                          ratio_value(75),
                                          ratio_value(125),
                                          ratio_value(30)),
                text=word.yes, manager=self.ui_manager, container=self.yn_window
            )
            self.no_yn_window_but = UIButton(
                relative_rect=pygame.Rect(ratio_value(155),
                                          ratio_value(75),
                                          ratio_value(125),
                                          ratio_value(30)),
                text=word.no, manager=self.ui_manager, container=self.yn_window
            )
            self.yn_winodw_label = UILabel(
                relative_rect=pygame.Rect(ratio_value(10),
                                          ratio_value(10),
                                          ratio_value(280),
                                          ratio_value(50)),
                text=f'{word.delete_game}?', manager=self.ui_manager, container=self.yn_window
            )

    def _delete_game(self):
        '''Удаляет игру'''
        game_saves_dict = json_func.read(json_path.game_saves)
        del game_saves_dict[self.delete_game_key]
        json_func.write(game_saves_dict, json_path.game_saves)
        self.game_selection_list.set_item_list(game_saves_dict)

    def _exit_func(self):
        '''Выход из игры'''
        pygame.quit()
        exit()
