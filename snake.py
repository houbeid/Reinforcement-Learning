class Snake:
    def __init__(self, start_pos=(5,5), initial_length=3, start_direction="RIGHT"):
        self.direction = start_direction
        # segments : liste de tuples (x, y), tête en premier
        self.segments = [(start_pos[0], start_pos[1] - i) for i in range(initial_length)]

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
        self.segments.pop()  # supprime la dernière cellule si pas de croissance

    def grow(self):
        self.segments.append(self.segments[-1])

    def shrink(self):
        if len(self.segments) > 1:
            self.segments.pop()

    def update_direction(self, new_direction):
        # éviter que le snake fasse demi-tour
        opposite = {"UP":"DOWN", "DOWN":"UP", "LEFT":"RIGHT", "RIGHT":"LEFT"}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    def head_collision(self, board):
        x, y = self.head_position()
        # collision mur
        if x < 0 or x >= board.width or y < 0 or y >= board.height:
            return True
        # collision avec corps
        if (x, y) in self.body_positions():
            return True
        return False

    def get_state(self, board):
        """Retourne l'état autour de la tête pour Q-learning"""
        head_x, head_y = self.head_position()
        state = []

        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }

        for dx, dy in directions.values():
            x, y = head_x + dx, head_y + dy
            if x < 0 or x >= board.width or y < 0 or y >= board.height:
                state.append("W")  # mur
            elif (x, y) in self.body_positions():
                state.append("S")  # corps
            elif (x, y) in [apple.position for apple in board.green_apples]:
                state.append("G")  # pomme verte
            elif (x, y) == board.red_apple.position:
                state.append("R")  # pomme rouge
            else:
                state.append(0)    # vide
        return tuple(state)
