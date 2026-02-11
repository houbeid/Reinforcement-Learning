import random

class Apple:
    def __init__(self, board_size, color=(0,255,0)):
        self.board_size = board_size
        self.color = color
        self.position = self.random_position()
    
    def random_position(self):
        # choisir une position aléatoire dans la grille
        x = random.randint(0, self.board_size - 1)
        y = random.randint(0, self.board_size - 1)
        return (x, y)
    
    def respawn(self, snake_segments, other_apples=[]):
        # générer une nouvelle position qui n'entre pas en collision
        while True:
            new_pos = self.random_position()
            if new_pos not in snake_segments and new_pos not in other_apples:
                self.position = new_pos
                break
