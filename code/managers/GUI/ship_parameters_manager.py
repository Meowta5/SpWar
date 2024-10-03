
from pygame import Rect
import pygame
from pygame_gui.elements import UILabel, UIDropDownMenu, UIButton, UISelectionList
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED

from code.function import ratio_value
import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager


class ShipParametersManager(InheritanceGUIManager):
    def __init__(self, ui_manager, gui_dict):
        super().__init__()

        self.gui_dict = gui_dict
        self.ui_manager = ui_manager

        self.gui_dict['ship_parameters'] = []
        #self.f = {}
        #self.f2 = ''
        

        self._create_buttons()
        self._create_selection_list()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        self.parameters_list.set_item_list(
            (
                word.strength, word.shield, word.restoring_shield, word.reactor, word.speed,
                word.recoil, word.recharge, word.damage, word.energy_distribution
            )
        )

    def check_event(self, event):
        '''Проверка событий GUI'''
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.return_but:
                return 'switch start_menu'

    def start(self):
        '''Инициализация всего необходимого для работы менеджера'''
        ...

    def _switch_logic(self):
        '''...'''
        #self.switch_sea_layer()

    def _create_buttons(self):
        '''Создание кнопок'''
        self.switch_but = UIButton(
            relative_rect=Rect(
                ratio_value(15), ratio_value(296), ratio_value(500), ratio_value(50)
            ), text=word.switch, manager=self.ui_manager
        )
        self.return_but = UIButton(
            relative_rect=Rect(
                ratio_value(100), ratio_value(525), ratio_value(200), ratio_value(50)
            ),
            text=word.return_, manager=self.ui_manager
        )
        self.gui_dict['ship_parameters'].append(self.switch_but)
        self.gui_dict['ship_parameters'].append(self.return_but)

    def _create_labels(self):
        '''Создание надписей'''
        ...

    def _create_selection_list(self):
        '''Создание меню выбора игры'''
        self.parameters_list = UISelectionList(
            relative_rect=Rect(
                ratio_value(15), ratio_value(15), ratio_value(500), ratio_value(276)
            ),
            item_list=(
                word.strength, word.shield, word.restoring_shield, word.reactor, word.speed,
                word.recoil, word.recharge, word.damage, word.energy_distribution
            ),
            manager=self.ui_manager
        )
        self.gui_dict['ship_parameters'].append(self.parameters_list)
