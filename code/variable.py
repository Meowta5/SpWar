
# В этом файле хранятся и обновляются переменные необходимые для работы игры

import pygame

import code.path.json_path as json_path
import code.json_function as json_func

# Инициализация переменных

# Константы
FPS_LIMIT = 30
INFO = pygame.display.Info()
DISPLAY_SIZE = (INFO.current_w, INFO.current_h)
EVENTUAL_SCREEN_SIZE = ((1200, 600), (1400, 700), (1600, 800), (1800, 900), DISPLAY_SIZE)


# Процедуры
def load_settings_json():
    '''Загружает настройки игры'''
    global settings
    global controls
    
    controls = json_func.read(json_path.controls)
    settings = json_func.read(json_path.settings)

    define_language()
    player_ship_move_state_update()
    move_player_helth_update()
    
    
def define_language():
    '''Определение языка'''
    global language
    language = settings['language']
    

def load_game_saves_json():
    '''Загружает сохраненные игры'''
    global game_saves
    game_saves = json_func.read(json_path.game_saves)


def screen_resolution_update():
    '''Обновление разрешения экрана'''
    global screen_size
    global topleft_main_screen
    global bottomright_main_screen
    global background_size_coeff
    
    screen_index = settings['screen_size_index']
    
    match screen_index:
        case 0:
            screen_size = (1200, 600)
            topleft_main_screen = (0, 0)
            bottomright_main_screen = (1200, 600)
        case 1:
            screen_size = (1400, 700)
            topleft_main_screen = (0, 0)
            bottomright_main_screen = (1400, 700)
        case 2:
            screen_size = (1600, 800)
            topleft_main_screen = (0, 0)
            bottomright_main_screen = (1600, 800)
        case 3:
            screen_size = (1800, 900)
            topleft_main_screen = (0, 0)
            bottomright_main_screen = (1800, 900)
        case 4:
            full_screen_width = INFO.current_w
            full_screen_hight = INFO.current_h
            screen_size = (full_screen_width, full_screen_hight)
            while full_screen_width < full_screen_hight * 2:
                full_screen_hight -= 1

            topleft_main_screen = ((INFO.current_w - full_screen_hight * 2) // 2,
                                    (INFO.current_h - full_screen_hight) // 2)
            bottomright_main_screen = (screen_size[0] - topleft_main_screen[0],
                                        screen_size[1] - (topleft_main_screen[1] * 2))
    background_size_coeff = bottomright_main_screen[0] / 4800


def player_ship_move_state_update():
    '''Обновление типа передвижения корабля (игрок)'''
    global player_ship_move_state
    player_ship_move_state = settings['player_move_state']


def move_player_helth_update():
    '''Опеределение передвижения прочности коробля и щита игрока'''
    global move_location
    move_location = settings['move_player_helth']


load_settings_json()
load_game_saves_json()
screen_resolution_update()
player_ship_move_state_update()
move_player_helth_update()
define_language()


# Переменные значения которых буду загружены позже
damnium_buy = bool()
versi_buy = bool()
celeritas_buy = bool()
libra_buy = bool()

damnium_param = dict()
versi_param = dict()
celeritas_param = dict()
libra_param = dict()

record = int()
money = int()
rupiy = int()
elerius = int()
duranty = int()
astrius = int()
