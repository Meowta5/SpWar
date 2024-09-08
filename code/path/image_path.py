
import os

curdir = os.path.dirname(__file__)
# Космические корабли

'''Текстуры Верси:'''

# Корабль
versi_ship_path = os.path.join(curdir, '../../data/images/ships/versi/ship.gif')

# Свет
versi_light_path = os.path.join(curdir, '../../data/images/ships/versi/light.gif')

# Лазер
versi_laser_path = os.path.join(curdir, '../../data/images/ships/versi/laser.gif')

# Турель
versi_turret_path = os.path.join(curdir, '../../data/images/ships/versi/turret.png')

# Снаряд турели
versi_turret_bullet_path = os.path.join(curdir, '../../data/images/ships/versi/bullet.png')


'''Текстуры Дамниум:'''

# Корабль
damnium_ship_path = os.path.join(curdir, '../../data/images/ships/damnium/ship.gif')

# Свет
damnium_light_path = os.path.join(curdir, '../../data/images/ships/damnium/light.gif')

# Снаряд
damnium_bullet_path = os.path.join(curdir, '../../data/images/ships/damnium/bullet.png')

'''Текстуры Либры'''

# Корабль
libra_ship_path = os.path.join(curdir, '../../data/images/ships/libra/ship.gif')

# Свет
libra_light_path = os.path.join(curdir, '../../data/images/ships/libra/light.gif')

# Снаряд
libra_bullet_path = os.path.join(curdir, '../../data/images/ships/libra/bullet.png')

'''Текстуры Целеритаса'''

# Свет
celeritas_light_path = os.path.join(curdir, '../../data/images/ships/celeritas/light.gif')

# Корабль
celeritas_ship_path = os.path.join(curdir, '../../data/images/ships/celeritas/ship.gif')

# Снаряд
celeritas_bullet_path = os.path.join(curdir, 'data/images/ships/celeritas/bullet.png')

'''Взрыв'''

# Корабль

ship_blast_path_one = os.path.join(curdir, '../../data/images/blasts/ship/versi.gif')

# Снаряд

bullet_blast_one_path = os.path.join(curdir, '../../data/images/blasts/bullet/blast1.gif')

bullet_blast_two_path = os.path.join(curdir, '../../data/images/blasts/bullet/blast2.gif')

# Астероид

asteroid_blast_one_path = os.path.join(curdir, '../../data/images/blasts/asteroid/blast1.gif')

'''Астероиды'''

asteroid_path_one = tuple([os.path.join(curdir, f'../../data/images/asteroids/asteroid{i}.png') for i in range(1, 3 + 1)])

'''Фоны'''
background_path_one = os.path.join(curdir, '../../data/images/backgrounds/background1.png')

load_screen_path = os.path.join(curdir, '../../data/images/backgrounds/load_screen.png')

'''Интерфейс'''

selection_menu_background_path_one = os.path.join(curdir, '../../data/images/selection_menu_image/basic_background.png')
