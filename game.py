from snake import Snake
from board import Board
from Apple import Apple


class Game:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self._init_game()

    def _init_game(self):
        self.snake = Snake(start_pos=(self.board_size // 2, self.board_size // 2), initial_length=3)
        self.board = Board(width=self.board_size, height=self.board_size, snake=self.snake)

        green1 = Apple(self.board)
        green2 = Apple(self.board, other_positions=[green1.position])
        self.board.green_apples = [green1, green2]
        self.board.red_apple = Apple(
            self.board,
            color=(255, 0, 0),
            other_positions=[green1.position, green2.position]
        )

        self.prev_distance     = None
        self.visited_positions = []   # historique des positions de la tête
        self.loop_penalty      = 0    # pénalité cumulative de boucle

    def reset(self):
        """Réinitialise le jeu pour un nouvel épisode."""
        self._init_game()

    def calculate_reward(self):
        head            = self.snake.head_position()
        green_positions = [g.position for g in self.board.green_apples]
        red_position    = self.board.red_apple.position

        # Distance à la pomme verte la plus proche
        if green_positions:
            closest_green = min(
                green_positions,
                key=lambda g: abs(g[0] - head[0]) + abs(g[1] - head[1])
            )
            dist_after = abs(closest_green[0] - head[0]) + abs(closest_green[1] - head[1])
        else:
            dist_after = None

        dist_before        = self.prev_distance
        self.prev_distance = dist_after

        # ---- Récompenses principales ----
        if head in green_positions:
            # Manger une pomme verte → reset de l'historique de boucle
            self.visited_positions = []
            self.loop_penalty      = 0
            reward = 10

        elif head == red_position:
            reward = -5

        else:
            # +2 si on se rapproche de la pomme verte, -2 si on s'éloigne
            if dist_before is not None and dist_after is not None:
                reward = 2 if dist_after < dist_before else -2
            else:
                reward = -2

        # ---- Pénalité de boucle ----
        # Vérifier si la tête était déjà dans les 20 dernières positions
        # AVANT d'ajouter la position actuelle → évite le faux positif
        if head in self.visited_positions[-20:]:
            self.loop_penalty -= 1
        else:
            self.loop_penalty = 0

        # Enregistrer la position APRÈS la vérification
        self.visited_positions.append(head)

        reward += self.loop_penalty

        return reward

    def step(self, action_direction):
        if action_direction is not None:
            self.snake.update_direction(action_direction)

        self.snake.move()

        # Collision mur ou corps → fin d'épisode
        if self.snake.head_collision(self.board):
            return self.snake.get_state(self.board), -10, True

        # Manger une pomme verte → grandir + respawn
        for green in self.board.green_apples:
            if self.snake.head_position() == green.position:
                self.snake.grow()
                other = (
                    [a.position for a in self.board.green_apples if a != green]
                    + [self.board.red_apple.position]
                )
                green.respawn(self.snake.segments, other_apples=other)

        # Manger la pomme rouge → rétrécir ou fin d'épisode
        if self.snake.head_position() == self.board.red_apple.position:
            if len(self.snake.segments) > 1:
                self.snake.shrink()
            else:
                return self.snake.get_state(self.board), -10, True
            self.board.red_apple.respawn(
                self.snake.segments,
                other_apples=[g.position for g in self.board.green_apples]
            )

        reward = self.calculate_reward()
        state  = self.snake.get_state(self.board)
        done   = False

        return state, reward, done

    def get_state(self):
        return self.snake.get_state(self.board)