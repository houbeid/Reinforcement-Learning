class Apple:
    def __init__(self, board, color=(0, 255, 0), other_positions=None):
        self.board = board
        self.color = color
        other_positions = other_positions or []
        self.position = self.board.random_empty_cell(
            self.board.snake.segments,
            other_apples=other_positions
        )

    def respawn(self, snake_segments, other_apples=[]):
        self.position = self.board.random_empty_cell(snake_segments, other_apples)
