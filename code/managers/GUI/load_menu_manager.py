
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

    def set_game_selection_list_items(self):
        self.game_selection_list.set_item_list([i for i in vb.game_saves.keys()])

    def check_event(self, event):
        '''Проверка событий GUI'''
        if not self.window_activ:
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.create_new_game_but:
                    return 'switch create_new_game'
                elif event.ui_element == self.load_game_but:
                    vb.game_save_key = self.game_selection_list.get_single_selection()
                    return 'switch start_menu'
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
                    self.yn_window.kill()

            rect = self.yn_window.get_abs_rect()
            if (rect.topleft[0] < 0
                or rect.bottomright[0] > vb.bottomright_main_screen[0]
                or rect.topleft[1] < 0
                or rect.bottomright[1] > vb.bottomright_main_screen[1]
                ): self.yn_window.set_position((ratio_value(450), ratio_value(225)))
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
        del vb.game_saves[self.delete_game_key]
        json_func.write(vb.game_saves, json_path.game_saves)
        self.set_game_selection_list_items()

    def _exit_func(self):
        '''Выход из игры'''
        pygame.quit()
        exit()
