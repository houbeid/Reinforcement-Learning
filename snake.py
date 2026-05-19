class Snake:
    def __init__(self, start_pos=(5, 5), initial_length=3,
                 start_direction="RIGHT"):
        self.direction = start_direction

        direction_offset = {
            "RIGHT": (-1, 0),
            "LEFT": (1, 0),
            "UP": (0, 1),
            "DOWN": (0, -1)
        }
        dx, dy = direction_offset[start_direction]
        self.segments = [
            (start_pos[0] + dx * i, start_pos[1] + dy * i)
            for i in range(initial_length)
        ]

    def head_position(self):
        return self.segments[0]

    def body_positions(self):
        return self.segments[1:]

    def move(self):
        head_x, head_y = self.head_position()
        if self.direction == "UP":
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1
        elif self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
            head_x += 1

        self.segments.insert(0, (head_x, head_y))
        self.segments.pop()

    def grow(self):
        self.segments.append(self.segments[-1])

    def shrink(self):
        if len(self.segments) > 1:
            self.segments.pop()

    def update_direction(self, new_direction):
        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    def head_collision(self, board):
        x, y = self.head_position()
        if x < 0 or x >= board.width or y < 0 or y >= board.height:
            return True
        if (x, y) in self.body_positions():
            return True
        return False

    def get_vision_string(self, board):
        """
        Retourne la vision du serpent sous forme de string multi-lignes
        pour affichage terminal (requis par le sujet).

        Format (4 directions depuis la tête) :
        - W = Wall (mur)
        - H = Snake Head (tête)
        - S = Snake body Segment (corps)
        - G = Green apple (pomme verte)
        - R = Red apple (pomme rouge)
        - 0 = Empty space (vide)
        """
        head_x, head_y = self.head_position()

        vision_range = 3
        vision_lines = []

        for dy in range(1, vision_range + 1):
            x, y = head_x, head_y - dy
            vision_lines.append(self._get_cell_char(x, y, board))

        left_chars = ""
        for dx in range(vision_range, 0, -1):
            x, y = head_x - dx, head_y
            left_chars += self._get_cell_char(x, y, board)

        right_chars = ""
        for dx in range(1, vision_range + 1):
            x, y = head_x + dx, head_y
            right_chars += self._get_cell_char(x, y, board)

        vision_lines.append(left_chars + "H" + right_chars)

        for dy in range(1, vision_range + 1):
            x, y = head_x, head_y + dy
            vision_lines.append(self._get_cell_char(x, y, board))

        return "\n".join(vision_lines)

    def _get_cell_char(self, x, y, board):
        """Retourne le caractère représentant une cellule."""
        if x < 0 or x >= board.width or y < 0 or y >= board.height:
            return "W"

        pos = (x, y)

        if pos in self.body_positions():
            return "S"

        green_positions = [g.position for g in board.green_apples]
        if pos in green_positions:
            return "G"

        if pos == board.red_apple.position:
            return "R"

        return "0"

    def get_state(self, board):
        """
        Retourne l'état numérique pour la Q-table (tuple de 15 valeurs).
        Utilisé pour l'apprentissage, PAS pour l'affichage.
        """
        head_x, head_y = self.head_position()
        state = []

        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        dir_order = ["UP", "RIGHT", "DOWN", "LEFT"]
        idx = dir_order.index(self.direction)

        moves = [
            directions[dir_order[idx]],
            directions[dir_order[(idx - 1) % 4]],
            directions[dir_order[(idx + 1) % 4]]
        ]

        for dx, dy in moves:
            x, y = head_x + dx, head_y + dy
            if x < 0 or x >= board.width or y < 0 or y >= board.height:
                state.append(1)
            elif (x, y) in self.body_positions():
                state.append(1)
            else:
                state.append(0)

        for d in ["UP", "DOWN", "LEFT", "RIGHT"]:
            state.append(1 if self.direction == d else 0)

        if board.green_apples:
            closest_green = min(
                board.green_apples,
                key=lambda g: (abs(g.position[0] - head_x) +
                               abs(g.position[1] - head_y))
            )
            gx, gy = closest_green.position
            state.append(1 if gx < head_x else 0)
            state.append(1 if gx > head_x else 0)
            state.append(1 if gy < head_y else 0)
            state.append(1 if gy > head_y else 0)
        else:
            state.extend([0, 0, 0, 0])

        apple_x, apple_y = board.red_apple.position
        state.append(1 if apple_x < head_x else 0)
        state.append(1 if apple_x > head_x else 0)
        state.append(1 if apple_y < head_y else 0)
        state.append(1 if apple_y > head_y else 0)

        return tuple(state)
