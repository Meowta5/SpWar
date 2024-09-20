
from sys import exit

import pygame
from pygame_gui import UIManager

import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.function import ratio_value
from code.object.inheritance_gui_manager import InheritanceGUIManager
from code.managers.GUI import (
    load_menu_manager, settings_manager, controls_manager, create_new_game_manager,
    start_menu_manager
)


class GUIManager(InheritanceGUIManager):
    def __init__(self, screen_manager, clock):
        super().__init__()
        self.gui_dict = {}

        # Экран
        self.screen_rect, self.screen = screen_manager.get_screen()
        self.screen_size_index = screen_manager.get_screen_size_index()
        self.screen_manager = screen_manager

        # Цикл событий
        self.clock = clock

        # Менеджер
        print('НАЧАТА ИНИЦИАЛИЗАЦИЯ МЕНЕДЖЕРА')
        self.ui_manager = UIManager(vb.screen_size, theme_path=json_path.gui_them)
        print('МЕНЕДЖЕР УСПЕШНО ИНИЦИАЛИЗИРОВАН')
        print('НАЧАТА ЗАГРУЗКА ИРРОР ТЕМЫ')
        self.ui_manager.create_new_theme(json_path.error_them)
        print('ИРРОР УСПЕШНО ТЕМА ЗАГРУЖЕНА')

        self.load_menu_manager = load_menu_manager.LoadMenuManager(
            self.ui_manager,  self.gui_dict
        )
        self.settings_manager = settings_manager.SettingsManager(
            self.ui_manager, screen_manager, self.screen_size_index, self.gui_dict
        )
        self.controls_manager = controls_manager.ControlsManager(
            self.ui_manager, clock, self.screen, self.screen_size_index, self.gui_dict
        )
        self.create_new_game_manager = create_new_game_manager.CreateNewGameManager(
            self.ui_manager, self.gui_dict
        )
        self.start_menu_manager = start_menu_manager.StartMenuManager(
            self.ui_manager, self.gui_dict
        )
        self.start_menu_manager.data_update()

        self.switch_sea_layer('load_menu')
        
    def run_gui(self):
        self.run = True
        while self.run:
            # Ограничение скорости цикла событий
            time_delta = self.clock.tick(vb.FPS_LIMIT) / 1000.0
            self.screen.fill((0, 0, 0))
            
            # Проверка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self._check_event(event)
                
            if self.layer == 'create_new_game':
                self.create_new_game_manager.update_and_draw(
                    False, self.screen, self.screen_rect
                )
            elif self.layer == 'start_menu':
                self.start_menu_manager.update_and_draw(self.screen, False)
            
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            
            # Обновление экрана
            pygame.display.update()

    def set_language(self, language):
        '''Устанавливает язык интерфейса GUI'''
        if language != 'ru' and language != 'en':
            raise
        data = json_func.read(json_path.settings)
        data['language'] = language
        json_func.write(data, json_path.settings)
        vb.load_settings_json()
        if language == 'ru':
            word.set_ru_language()
        else:
            word.set_en_language()
        
        self.load_menu_manager.set_language()
        self.settings_manager.set_language()
        self.controls_manager.set_language()
        self.create_new_game_manager.set_language()
        
        self.switch_sea_layer(self.layer)
        
    def set_text_size(self):
        '''...'''
        theme = json_func.read(json_path.gui_them)

        theme['label']['font']['size'] = ratio_value(20)
        theme['#error_label']['font']['size'] = ratio_value(20)
        
        theme['button']['font']['size'] = ratio_value(20)
        
        theme['drop_down_menu.#drop_down_options_list']['misc']['list_item_height'] = (
            f'{int(ratio_value(30))}')
        json_func.write(theme, json_path.gui_them)

    def start(self, gui_manager):
        '''Инициализация всего необходимого для работы менеджера'''
        
        print(f'СТАРТ GUI МЕНЕДЖЕРА | {gui_manager=}')
        
        self.load_menu_manager.start(gui_manager)
        self.settings_manager.start(gui_manager)
    
    def _check_event(self, event):
        '''Проверка событий GUI'''
        if self.layer == 'load_menu':
            if not (ev := self.load_menu_manager.check_event(event)) is None:
                if ev == 'switch settings':
                    self.switch_sea_layer('settings')
                elif ev == 'switch create_new_game':
                    self.switch_sea_layer('create_new_game')
                    self.create_new_game_manager.there_is_name_label.hide()
                elif ev[0] == 'switch start_menu' and not ev[1] is None:
                    self.start_menu_manager.start(vb.game_saves[ev[1]], self.screen_rect)
                    self.switch_sea_layer('start_menu')
        elif self.layer == 'settings':
            if not (ev := self.settings_manager.check_event(event)) is None:
                if ev == 'switch load_menu':
                    self.switch_sea_layer('load_menu')
                elif ev == 'switch controls':
                    self.switch_sea_layer('controls')
        elif self.layer == 'controls':
            if not (ev := self.controls_manager.check_event(event)) is None:
                if ev == 'switch settings':
                    self.switch_sea_layer('settings')
        elif self.layer == 'create_new_game':
            if not (ev := self.create_new_game_manager.check_event(event)) is None:
                if ev == 'switch load_menu':
                    self.switch_sea_layer('load_menu')
                elif ev[0] == 'switch start_menu':
                    self.start_menu_manager.start(vb.game_saves[ev[1]], self.screen_rect)
                    self.load_menu_manager.set_game_selection_list_items()
                    self.switch_sea_layer('start_menu')
                self.create_new_game_manager.update_and_draw(True, self.screen, self.screen_rect)
        elif self.layer == 'start_menu':
            if not (ev := self.start_menu_manager.check_event(event)) is None:
                if ev == 'switch load_menu':
                    self.switch_sea_layer('load_menu')
        self.ui_manager.process_events(event)
