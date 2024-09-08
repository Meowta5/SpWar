
# Класс фона

import pygame
import code.variable as vb


class SpaceBackground(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=position)

        self.x_pos = position[0]

    def move_animation(self):
        self.rect.x -= 14
        if self.rect.x <= self.x_pos - vb.bottomright_main_screen[0]:
            self.rect.x = self.x_pos

    def update(self):
        self.move_animation()


class BasicSpaceBackground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(vb.screen_size)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(0, 0))
