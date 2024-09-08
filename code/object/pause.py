import pygame

class PauseBackground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
        self.image.fill((0, 0, 0))
        self.image.set_alpha(100)
        self.rect = self.image.get_rect(topleft=(0, 0))
        