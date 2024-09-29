
import pygame
from pygame_gui.elements import UILabel, UIDropDownMenu, UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED

from code.function import ratio_value
import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word
from code.object.inheritance_gui_manager import InheritanceGUIManager


class ControlsManager(InheritanceGUIManager):
    def __init__(self, ui_manager, clock, screen, screen_size_index, gui_dict):
        super().__init__()
        self.gui_dict = gui_dict
        self.screen_size_index = screen_size_index
        self.ui_manager = ui_manager
        self.clock = clock
        self.screen = screen
        
        self.gui_dict['controls'] = []
        self.torun = False
        
        self._create_buttons()
        self._create_labels()
        self._create_drop_menu()

    def set_language(self):
        '''Устанавливает язык интерфейса GUI'''
        
        self.move_state_reset_but.set_text(word.reset)
        self.move_helth_reset_but.set_text(word.reset)
        self.up_move_reset_but.set_text(word.reset)
        self.down_move_reset_but.set_text(word.reset)
        self.left_move_reset_but.set_text(word.reset)
        self.right_move_reset_but.set_text(word.reset)
        self.shoot_reset_but.set_text(word.reset)
        
        self.move_state_label.set_text(word.player_ship_move_state)
        self.move_helth_label.set_text(word.helth_move)
        self.up_move_label.set_text(word.up_move)
        self.down_move_label.set_text(word.down_move)
        self.left_move_label.set_text(word.left_move)
        self.right_move_label.set_text(word.right_move)
        self.shoot_label.set_text(word.shoot)

        self._replacement_drop_menu()

    def check_event(self, event):
        '''Проверка событий GUI'''
        if event.type == UI_BUTTON_PRESSED:
            if event.ui_element == self.return_but:
                return 'switch settings'
            # Движение вперед
            elif event.ui_element == self.up_move_but and not self.torun:
                self._change_and_check_control(self.up_move_but, 'player_up_move')
            elif event.ui_element == self.up_move_reset_but and not self.torun:
                self._change_control(self.up_move_but, 'player_up_move', 119)
            # Движение назад
            elif event.ui_element == self.down_move_but and not self.torun:
                self._change_and_check_control(self.down_move_but, 'player_down_move')
            elif event.ui_element == self.down_move_reset_but and not self.torun:
                self._change_control(self.down_move_but, 'player_down_move', 115)
            # Движение влево
            elif event.ui_element == self.left_move_but and not self.torun:
                self._change_and_check_control(self.left_move_but, 'player_left_move')
            elif event.ui_element == self.left_move_reset_but and not self.torun:
                self._change_control(self.left_move_but, 'player_left_move', 97)
            # Движение вправо
            elif event.ui_element == self.right_move_but and not self.torun:
                self._change_and_check_control(self.right_move_but, 'player_right_move')
            elif event.ui_element == self.right_move_reset_but and not self.torun:
                self._change_control(self.right_move_but, 'player_right_move', 100)
            # Стрелять
            elif event.ui_element == self.shoot_but and not self.torun:
                self._change_and_check_control(self.shoot_but, 'player_shoot')
            elif event.ui_element == self.shoot_reset_but and not self.torun:
                self._change_control(self.shoot_but, 'player_shoot', 32)
        
        elif event.type == UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.move_state_menu and event.text != vb.settings[
                'player_move_state']:
                vb.settings['player_move_state'] = int(event.text) - 1
                json_func.write(vb.settings, json_path.settings)
            elif event.ui_element == self.move_helth_menu:
                if event.text == word.on and vb.settings['move_player_helth'] != True:
                    vb.settings['move_player_helth'] = True
                elif event.text ==  word.off and vb.settings['move_player_helth'] != False:
                    vb.settings['move_player_helth'] = False
                json_func.write(vb.settings, json_path.settings)

    def start(self):
        '''Инициализация всего необходимого для работы менеджера'''

    def _create_buttons(self):
        '''Создание кнопок'''
        self.return_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(100), ratio_value(525)),
                                      (ratio_value(200), ratio_value(50))),
            text=word.return_, manager=self.ui_manager
        )
        
        # Схема передвижения игрока
        self.move_state_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(25)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        
        # Движение прочности игрока
        self.move_helth_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(85)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        
        # Движение вперед
        self.up_move_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(145)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        self.up_move_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(145)),
                                      (ratio_value(200), ratio_value(50))),
            text=pygame.key.name(vb.controls['player_up_move']), manager=self.ui_manager
        )

        # Движение назад
        self.down_move_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(205)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        self.down_move_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(205)),
                                      (ratio_value(200), ratio_value(50))),
            text=pygame.key.name(vb.controls['player_down_move']), manager=self.ui_manager
        )

        # Движение влево
        self.left_move_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(265)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        self.left_move_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(265)),
                                      (ratio_value(200), ratio_value(50))),
            text=pygame.key.name(vb.controls['player_left_move']), manager=self.ui_manager
        )
        
        # Движение вправо
        self.right_move_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(325)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        self.right_move_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(325)),
                                      (ratio_value(200), ratio_value(50))),
            text=pygame.key.name(vb.controls['player_right_move']), manager=self.ui_manager
        )

        # Стрелять
        self.shoot_reset_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(545), ratio_value(385)),
                                      (ratio_value(100), ratio_value(50))),
            text=word.reset, manager=self.ui_manager
        )
        self.shoot_but = UIButton(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(385)),
                                      (ratio_value(200), ratio_value(50))),
            text=pygame.key.name(vb.controls['player_shoot']), manager=self.ui_manager
        )
        
        # Добавление элементов в список
        self.gui_dict['controls'].append(self.return_but)
        self.gui_dict['controls'].append(self.move_state_reset_but)
        self.gui_dict['controls'].append(self.move_helth_reset_but)
        self.gui_dict['controls'].append(self.up_move_reset_but)
        self.gui_dict['controls'].append(self.up_move_but)
        self.gui_dict['controls'].append(self.down_move_reset_but)
        self.gui_dict['controls'].append(self.down_move_but)
        self.gui_dict['controls'].append(self.left_move_reset_but)
        self.gui_dict['controls'].append(self.left_move_but)
        self.gui_dict['controls'].append(self.right_move_reset_but)
        self.gui_dict['controls'].append(self.right_move_but)
        self.gui_dict['controls'].append(self.shoot_reset_but)
        self.gui_dict['controls'].append(self.shoot_but)

    def _create_labels(self):
        '''Создание надписей'''
        self.move_state_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(25)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.player_ship_move_state, manager=self.ui_manager
        )
        self.move_helth_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(85)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.helth_move, manager=self.ui_manager
        )
        self.up_move_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(145)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.up_move, manager=self.ui_manager
        )
        self.down_move_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(205)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.down_move, manager=self.ui_manager
        )
        self.left_move_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(265)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.left_move, manager=self.ui_manager
        )
        self.right_move_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(325)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.right_move, manager=self.ui_manager
        )
        self.shoot_label = UILabel(
            relative_rect=pygame.Rect((ratio_value(25), ratio_value(385)),
                                      (ratio_value(300), ratio_value(50))),
            text=word.shoot, manager=self.ui_manager
        )
        
        self.gui_dict['controls'].append(self.move_state_label)
        self.gui_dict['controls'].append(self.move_helth_label)
        self.gui_dict['controls'].append(self.up_move_label)
        self.gui_dict['controls'].append(self.down_move_label)
        self.gui_dict['controls'].append(self.left_move_label)
        self.gui_dict['controls'].append(self.right_move_label)
        self.gui_dict['controls'].append(self.shoot_label)

    def _create_drop_menu(self):
        '''Создаение выдающих меню'''
        self.move_helth_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(85)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=(word.on, word.off),
            starting_option=(word.on, word.off)[0 if vb.settings['move_player_helth'] else 1],
            manager=self.ui_manager
        )
        self.move_state_menu = UIDropDownMenu(
            relative_rect=pygame.Rect((ratio_value(335), ratio_value(25)),
                                      (ratio_value(200), ratio_value(50))),
            options_list=['1', '2', '3'], starting_option=['1', '2', '3'][
                vb.settings['player_move_state']], manager=self.ui_manager
        )
        
        self.gui_dict['controls'].append(self.move_helth_menu)
        self.gui_dict['controls'].append(self.move_state_menu)

    def _replacement_drop_menu(self):
        '''Удаляет прошлое и создает новые меню выпадающие вниз'''
        self.gui_dict['controls'].remove(self.move_helth_menu)
        self.move_helth_menu.kill()
        
        self.gui_dict['controls'].remove(self.move_state_menu)
        self.move_state_menu.kill()
        
        self._create_drop_menu()

    def _change_and_check_control(self, button, key):
        '''Изменяет клавишу для определенного действия и изменяет текст на кнопке'''
        self.torun = True
        self.return_but.hide()
        button.set_text(word.press_key)
        
        while self.torun:
            # Ограничение скорости цикла событий
            time_delta = self.clock.tick(vb.FPS_LIMIT) / 1000.0
            
            # Проверка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                elif event.type == pygame.KEYDOWN:
                    self.torun = False
                    self.return_but.show()
                    button.set_text(pygame.key.name(event.key))
                    vb.controls[key] = event.key
                    json_func.write(vb.controls, json_path.controls)
                    break
    
                self.check_event(event)
            
            self.screen.fill((0, 0, 0))
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            
            # Обновление экрана
            pygame.display.update()

    def _change_control(self, button, path, mean):
        '''Изменяет управление и изменяет текст на кнопке'''
        
        button.set_text(pygame.key.name(mean))
        vb.controls[path] = mean
        json_func.write(vb.controls, json_path.controls)
