
import pygame
from pygame_gui.elements import UILabel, UIDropDownMenu, UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED

from code.function import ratio_value
import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager


class SelectShipManager(InheritanceGUIManager):
    def __init__(self, ui_manager, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.ui_manager = ui_manager
        
        self.gui_dict['select_ship'] = []
        
    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        
    def check_event(self):
        '''Проверка событий GUI'''

    def start(self):
        '''Инициализация всего необходимого для работы менеджера'''

    def _create_buttons(self):
        '''Создание кнопок'''
        
    def _create_drop_menu(self):
        '''Создаение выдающих меню'''
        
    def _create_drop_menu(self):
        ...
