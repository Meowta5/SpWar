
from typing import List

import pygame
from PIL import ImageSequence, Image

import code.variable as vb
import code.path.json_path as json_path
import code.json_function as json_func


def ratio_value(base_value) -> float:
    '''Опеределение скорости'''
    return vb.bottomright_main_screen[0] * base_value / 1200


def player_ship_move_state_change(state: int) -> None:
    '''Изменение схемы управления игрока'''
    vb.settings['player_move_state'] = state
    json_func.write(vb.settings, json_path.settings)




def load_image(path: str, size: float, convert_alpha: bool=True) -> pygame.surface.Surface:
    '''Принимает путь и размер изображения'''
    if convert_alpha:
        image = pygame.transform.rotozoom(
            pygame.image.load(path).convert_alpha(),
            0, size
        )
    else:
        image = pygame.transform.rotozoom(
            pygame.image.load(path).convert(),
            0, size
        )
    return image


def pil_image_to_surface(pil_image) -> pygame.Surface:
    mode, size, data = pil_image.mode, pil_image.size, pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def load_gif(path, size) -> List[pygame.Surface]:
    pil_image = Image.open(path)
    frames = []
    if pil_image.format == "GIF" and pil_image.is_animated:
        for frame in ImageSequence.Iterator(pil_image):
            pygame_image = pil_image_to_surface(frame.convert("RGBA"))
            frames.append(pygame.transform.rotozoom(pygame_image, 0, size))
    else:
        frames.append(pygame.transform.rotozoom(pil_image_to_surface(pil_image), 0, size))
    return frames
