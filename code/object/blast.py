
# Все классы связанные с игроком
from code.object import game_object

class Blast(game_object.GameObject):
    def __init__(self, sea_area_rect, image_tuple, position, speed=0.55):
        super().__init__(image_tuple, position)

        self.speed = speed
        
        if sea_area_rect.colliderect(self.rect):
            self.position_kill = False
        else:
            self.position_kill = True
            
    def killer(self):
        if self.image_index == 0 or self.position_kill:
            self.kill()
        
    def update(self):
        self.animation(self.speed)
        self.killer()
        