from code.object import game_object


class Light(game_object.GameObject):
    def __init__(self, image_tuple, position):
        super().__init__(image_tuple, position)

    def killer(self, light_live):
        '''Уничтожение света'''
        if not light_live:
            self.kill()
    
    def rotate_behind_object(self, position, player_angle_state):
        '''Поворот и движение света за объектом'''
        if player_angle_state == 1 or player_angle_state == 2:
            self.image, self.rect = self.rotate_towards_cursor(self.original_image, self.rect)
            
        self.rect.center = position
    