class Apple:
    def __init__(self, board, color=(0,255,0)):
        self.board = board
        self.color = color
        self.position = self.board.random_empty_cell(self.board.snake.segments)

    def respawn(self, snake_segments, other_apples=[]):
        self.position = self.board.random_empty_cell(snake_segments, other_apples)