import pygame
import pygame_gui
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        self.ui_manager = pygame_gui.UIManager((1200, 600))
        
        self.window = UIWindow(pygame.Rect((450, 225), (300, 150)),
                               manager=self.ui_manager,
                               window_display_title='Дополнительное окно',
                               object_id='#custom_window')
        
        self.button1 = UIButton(relative_rect=pygame.Rect((20, 75), (125, 30)),
                                text='Кнопка 1',
                                manager=self.ui_manager,
                                container=self.window,
                                object_id='#button1')
        
        self.button2 = UIButton(relative_rect=pygame.Rect((155, 75), (125, 30)),
                                text='Кнопка 2',
                                manager=self.ui_manager,
                                container=self.window,
                                object_id='#button2')
        self.button3 = UIButton(relative_rect=pygame.Rect((155, 75), (125, 30)),
                                text='Кнопка 3',
                                manager=self.ui_manager,
                                object_id='#button3')
        
    def process_events(self, event):
        super().process_events(event)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button1:
                print("Кнопка 1 нажата")
            elif event.ui_element == self.button2:
                print("Кнопка 2 нажата")
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            time_delta = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                self.ui_manager.process_events(event)
            
            self.ui_manager.update(time_delta)
            
            self.screen.fill((0, 0, 0))
            self.ui_manager.draw_ui(self.screen)
            pygame.display.flip()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
