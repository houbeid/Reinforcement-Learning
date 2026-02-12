# game.py
from snake import Snake
from board import Board
from Apple import Apple

class Game:
    def __init__(self, board_size=10):
        self.snake = Snake(start_pos=(board_size//2, board_size//2), initial_length=3)
        self.board = Board(width=board_size, height=board_size, snake=self.snake)

        # Créer pommes
        self.board.green_apples = [Apple(self.board), Apple(self.board)]
        self.board.red_apple = Apple(self.board, color=(255,0,0))

    def calculate_reward(self):
        head = self.snake.head_position()
        if head in [g.position for g in self.board.green_apples]:
            return 10
        elif head == self.board.red_apple.position:
            return -5
        else:
            return -1

    def step(self, action_direction):
         # 1. Mettre à jour direction seulement si action est valide
        if action_direction is not None:
            self.snake.update_direction(action_direction)

        # 2. Déplacer le snake
        self.snake.move()

        # 3. Collision
        if self.snake.head_collision(self.board):
            return self.snake.get_state(self.board), -10, True  # game over

        # 4. Vérifier pommes vertes
        for green in self.board.green_apples:
            if self.snake.head_position() == green.position:
                self.snake.grow()
                green.respawn(self.snake.segments, other_apples=[a.position for a in self.board.green_apples if a != green] + [self.board.red_apple.position])

        # 5. Vérifier pomme rouge
        if self.snake.head_position() == self.board.red_apple.position:
            if len(self.snake.segments) > 1:
                self.snake.shrink()
            else:
                return self.snake.get_state(self.board), -10, True  # game over
            self.board.red_apple.respawn(self.snake.segments, other_apples=[g.position for g in self.board.green_apples])

        # 6. Reward et state
        reward = self.calculate_reward()
        state = self.snake.get_state(self.board)
        done = False

        return state, reward, done

    def get_state(self):
        return self.snake.get_state(self.board)
