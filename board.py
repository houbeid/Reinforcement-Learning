import random

class Board:
    def __init__(self, width=10, height=10, snake=None):
        self.width = width
        self.height = height
        self.snake = snake
        self.green_apples = []
        self.red_apple = None

    def random_empty_cell(self, snake_segments, other_apples=[]):
        empty_cells = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in snake_segments and (x, y) not in other_apples
        ]
        return random.choice(empty_cells)