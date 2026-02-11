class Snake:
    def __init__(self, start_pos=(5,5), initial_length=3, start_direction="UP"):
        self.direction = start_direction     # direction initiale
        self.segments = [(start_pos[0], start_pos[1] - i) for i in range(initial_length)]  # liste de tuples (x, y)

    def move(self):
        head_x, head_y = self.segments[0]

        # mise à jour de la tête selon la direction
        if self.direction == "UP":
            head_y -= 1
        elif self.direction == "DOWN":
            head_y += 1
        elif self.direction == "LEFT":
            head_x -= 1
        elif self.direction == "RIGHT":
            head_x += 1

        # ajouter nouvelle tête
        self.segments.insert(0, (head_x, head_y))
        # retirer la dernière cellule (sauf si on a mangé une pomme)
        self.segments.pop()

    def grow(self):
        # ajouter un segment à la queue
        self.segments.append(self.segments[-1])

    def change_direction(self, new_direction):
        # éviter de se retourner
        opposite = {"UP":"DOWN", "DOWN":"UP", "LEFT":"RIGHT", "RIGHT":"LEFT"}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

    def head(self):
        return self.segments[0]
    
    def check_wall_collision(self, board_size):
        head_x, head_y = self.head()
        # si la tête est en dehors de la grille
        if head_x < 0 or head_x >= board_size or head_y < 0 or head_y >= board_size:
            return True
        return False
