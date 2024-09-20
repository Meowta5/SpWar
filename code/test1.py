import pygame
import pygame_gui

# Инициализация Pygame
pygame.init()

# Установка размеров окна
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Создание менеджера интерфейса с основной темой
manager = pygame_gui.UIManager(window_size, theme_path='../data/json_files/theme_one.json')

# Создание кнопки с темой theme_one
button1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 100), (150, 50)),
    text='Кнопка 1',
    manager=manager,
    object_id=pygame_gui.core.ObjectID(class_id='@theme_one', object_id='#button1')
)

# Загрузка дополнительной темы и создание кнопки с темой theme_two
button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((300, 100), (150, 50)),
    text='Кнопка 2',
    manager=manager,
    object_id=pygame_gui.core.ObjectID(class_id='@theme_two', object_id='#button2')
)

# Основной игровой цикл
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Обработка событий интерфейса
        manager.process_events(event)

    # Обновление интерфейса
    manager.update(time_delta)

    # Отрисовка интерфейса
    screen.fill((0, 0, 0))
    manager.draw_ui(screen)

    # Обновление экрана
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()
