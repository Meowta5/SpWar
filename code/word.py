
import code.variable as vr

new_game = ''
load_game = ''
delete_game = ''
guide = ''
exit = ''
settings = ''
reset_settings = ''
reset = ''
controls = ''
player_ship_move_state = ''
up_move = ''
down_move = ''
left_move = ''
right_move = ''
shoot = ''
contininue = ''
full_screen = ''
screen_size = ''
helth_move = ''
language = ''
en = ''
ru = ''
lmb = ''
mmb = ''
rbm = ''
return_ = ''
save = ''
on = ''
off = ''
yes = ''
no = ''
done = ''
press_key = ''
difficulty = ''
easy = ''
medium = ''
hard = ''
ship = ''
damnium = ''
libra = ''
celeritas = ''
versi = ''
random = ''
input_name_game = ''
there_is_name = ''

def set_ru_language():
    '''Устанавливает русский язык'''
    ru_dict = {
    'new_game': 'Новая игра',
    'load_game': 'Загрузить игру',
    'delete_game': 'Удалить игру',
    'guide': 'Обучение',
    'exit': 'Выход',
    'settings': 'Настройки',
    'reset_settings': 'Сбросить настройки',
    'reset': 'Сбросить',
    'controls': 'Управление',
    'player_ship_move_state': 'Способ движения игрока',
    'up_move': 'Движение вперед',
    'down_move': 'Движение назад',
    'left_move': 'Движение влево',
    'right_move': 'Движение вправо',
    'shoot': 'Стрелять',
    'contininue': 'Продолжить',
    'full_screen': 'Полный экран',
    'screen_size': 'Размер окна',
    'helth_move': 'Движение прочности игрока',
    'language': 'Язык',
    'en': 'Английский',
    'ru': 'Русский',
    'lmb': 'ЛКМ',
    'mmb': 'СКМ',
    'rbm': 'ПКМ',
    'return_': 'Назад',
    'save': 'Сохранить',
    'on': 'ВКЛ',
    'off': 'ВЫКЛ',
    'yes': 'Да',
    'no': 'Нет',
    'done': 'Готово',
    'press_key': 'Нажмите клавишу',
    'difficulty': 'Сложность',
    'easy': 'Легко',
    'medium': 'Средне',
    'hard': 'Сложно',
    'ship': 'Корабль',
    'damnium': 'Дамниум',
    'libra': 'Либра',
    'celeritas': 'Целеритас',
    'versi': 'Верси',
    'random': 'Случайный',
    'input_name_game': 'Введите название игры',
    'there_is_name': 'Игра с таким названием уже существует'
    }
    for key, value in ru_dict.items():
        globals()[key] = value


def set_en_language():
    '''Устанавливает английский язык'''
    en_dict = {
    'new_game': 'New game',
    'load_game': 'Load game',
    'delete_game': 'Delete game',
    'guide': 'Guide',
    'exit': 'Exit',
    'settings': 'Settings',
    'reset_settings': 'Reset settings',
    'reset': 'Reset',
    'controls': 'Controls',
    'player_ship_move_state': 'Player ship move state',
    'up_move': 'Up move',
    'down_move': 'Down move',
    'left_move': 'Left move',
    'right_move': 'Right move',
    'shoot': 'Shoot',
    'contininue': 'Contininue',
    'full_screen': 'Full screen',
    'screen_size': 'Window size',
    'helth_move': 'Move player helth',
    'language': 'Language',
    'en': 'English',
    'ru': 'Russian',
    'lmb': 'LMB',
    'mmb': 'MMB',
    'rbm': 'RMB',
    'return_': 'Return',
    'save': 'Save',
    'on': 'ON',
    'off': 'OFF',
    'yes': 'Yes',
    'no': 'No',
    'done': 'Done',
    'press_key': 'Press the key',
    'difficulty': 'Difficulty',
    'easy': 'Easy',
    'medium': 'Medium',
    'hard': 'Hard',
    'ship': 'Ship',
    'damnium': 'Damnium',
    'libra': 'Libra',
    'celeritas': 'Celeritas',
    'versi': 'Versi',
    'random': 'Random',
    'input_name_game': 'Enter the name of the game',
    'there_is_name': 'There is already a game with this name'
    }
    for key, value in en_dict.items():
        globals()[key] = value


if vr.language == 'ru':
    set_ru_language()
elif vr.language == 'en':
    set_en_language()
else:
    raise
