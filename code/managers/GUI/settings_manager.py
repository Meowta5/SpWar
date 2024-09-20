
import pygame
from pygame_gui.elements import UILabel, UIDropDownMenu, UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED

from code.function import ratio_value
import code.variable as vb
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager

class SettingsManager(InheritanceGUIManager):
    def __init__(self, ui_manager, screen_manager, screen_size_index, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.screen_size_index = screen_size_index
        self.ui_manager = ui_manager
        self.screen_manager = screen_manager
        
        self.gui_dict['settings'] = []
        
        self._create_buttons()
        self._create_labels()
        self._create_drop_menu()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        self.return_but.set_text(word.return_)
        self.controls_but.set_text(word.controls)
        
        self.scr_size_label.set_text(word.screen_size)
        self.language_menu_label.set_text(word.language)
        
        self._replacement_drop_menu()
        
    def check_event(self, event):
        '''Проверка событий GUI'''
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element ==  self.return_but:
                return 'switch load_menu'
            elif event.ui_element ==  self.controls_but:
                return 'switch controls'
            
        elif event.type == UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.scr_size_menu:
                for i in range(5):
                    if self._drop_down_menu_screen_size(event.text, i, self.gui_manager):
                        break
                
            elif event.ui_element == self.language_menu:
                if event.text == word.ru and vb.language != 'ru':
                    self.gui_manager.set_language('ru')
                elif event.text == word.en and vb.language != 'en':
                    self.gui_manager.set_language('en')

    def start(self, gui_manager):
        '''Инициализация всего необходимого для работы менеджера'''
        self.gui_manager = gui_manager

    def _create_buttons(self):
        '''Создание кнопок'''
        self.return_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(100), ratio_value(525)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.return_, manager=self.ui_manager
        )
        self.controls_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(285), ratio_value(170)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.controls, manager=self.ui_manager
        )
        self.gui_dict['settings'].append(self.return_but)
        self.gui_dict['settings'].append(self.controls_but)
        
    def _create_labels(self):
        '''Создание надписей'''
        self.scr_size_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(50)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.screen_size, manager=self.ui_manager
        )
        self.language_menu_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(75), ratio_value(110)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.language, manager=self.ui_manager
        )
        
        self.gui_dict['settings'].append(self.scr_size_label)
        self.gui_dict['settings'].append(self.language_menu_label)
    
    def _create_drop_menu(self):
        '''Создаение выдающих меню'''
        size_scr_tuple = ('1200x600', '1400x700', '1600x800','1800x900', word.full_screen)
        self.scr_size_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((ratio_value(285), ratio_value(50)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=size_scr_tuple,
            starting_option=size_scr_tuple[self.screen_size_index], manager=self.ui_manager
        )
        
        if vb.language == 'ru':
            start_index = 0
        elif vb.language == 'en':
            start_index = 1
            
        self.language_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((ratio_value(285), ratio_value(110)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=(word.ru, word.en),
            starting_option=(word.ru, word.en)[start_index], manager=self.ui_manager
        )
        self.gui_dict['settings'].append(self.scr_size_menu)
        self.gui_dict['settings'].append(self.language_menu)
        
    def _replacement_drop_menu(self):
        '''Удаляет прошлое и создает новые меню выпадающие вниз'''
        self.gui_dict['settings'].remove(self.scr_size_menu)
        self.scr_size_menu.kill()
        
        self.gui_dict['settings'].remove(self.language_menu)
        self.language_menu.kill()
        
        self._create_drop_menu()
        