
from pygame_gui import UIManager

from code.function import ratio_value
import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func
import code.word as word

class InheritanceGUIManager:
    def __init__(self) -> None:
        self.layer = ''
        
        self.ui_manager = UIManager(vb.screen_size, theme_path=json_path.gui_them)
        
    def visible_false_gui(self):
        '''Делает все элементы GUI невидимыми'''
        for _, il in self.gui_dict.items():
            for i in il:
                i.hide()

    def size_pos_update(self, l_scr_i):
        for _, el in self.gui_dict.items():
            for i in el:
                r = i.get_abs_rect()
                i.set_position(
                    (ratio_value(r.x / vb.EVENTUAL_SCREEN_SIZE[l_scr_i][0] * 1200),
                    ratio_value(r.y / vb.EVENTUAL_SCREEN_SIZE[l_scr_i][0] * 1200))
                )
                i.set_dimensions(
                    (ratio_value(r.right - r.left) / vb.EVENTUAL_SCREEN_SIZE[l_scr_i][0] * 1200,
                    ratio_value(r.bottom - r.top) / vb.EVENTUAL_SCREEN_SIZE[l_scr_i][0] * 1200)
                )
                i.rebuild()

    def switch_sea_layer(self, key):
        '''Переключает видимые части интрефейса'''
        self.visible_false_gui()
        for el in self.gui_dict[key]:
            el.show()
        self.layer = key
        
    def _drop_down_menu_screen_size(self, text, index):
        '''Изменяет размер параметров выпадающих меню'''
        
        size_scr_list = ['1200x600', '1400x700', '1600x800','1800x900', word.full_screen]
        if text == size_scr_list[index] and self.screen_size_index != index:
            
            sc_size = self.screen_manager.screen_resolution_change(index)
            self.ui_manager.set_window_resolution(sc_size)
            last_screen_size_index = self.screen_size_index
            self.screen_size_index = self.screen_manager.get_screen_size_index()

            self.size_pos_update(last_screen_size_index)
            
            theme = json_func.read(json_path.gui_them)
            theme['label']['font']['size'] = ratio_value(20)
            theme['button']['font']['size'] = ratio_value(20)
            theme['drop_down_menu.#drop_down_options_list']['misc']['list_item_height'] = (
                f'{int(ratio_value(30))}')
            json_func.write(theme, json_path.gui_them)
            
            return True
        else:
            return False
