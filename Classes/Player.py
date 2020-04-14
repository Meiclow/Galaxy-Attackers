from .Map import Map
from .Position import Position


class Player:
    def __init__(self, speed_vector: Position, max_hp, damage, position: Position, bullet_type=0):
        self.speed_vector = speed_vector
        self.damage = damage
        self.hp = max_hp
        self.bullet_type = bullet_type
        self.position = position

    def shoot(self):
        return self.bullet_type

    def move(self):
        self.position = Position(self.position.x + self.speed_vector.x, self.position.y + self.speed_vector.y)

    def take_damage(self, damage):
        self.hp -= damage

    def get_position(self):
        return self.getPosition
