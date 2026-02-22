import pygame
import pickle
from game import Game
import sys

# -------------------- INITIALISATION PYGAME --------------------
pygame.init()

cell_size = 40
board_size = 10
screen = pygame.display.set_mode((cell_size*board_size, cell_size*board_size))
pygame.display.set_caption("Learn2Slither RL - Non Learning")
clock = pygame.time.Clock()

actions = ["UP", "DOWN", "LEFT", "RIGHT"]

# -------------------- CHARGER LA Q-TABLE --------------------
q_table_file = "q_table_100.pkl"  # changer selon ton modèle
with open(q_table_file, "rb") as f:
    Q = pickle.load(f)

# -------------------- FONCTION POUR OBTENIR LES Q-VALUES --------------------
def get_Q(state):
    if state not in Q:
        # Si état jamais vu → toutes les actions = 0
        Q[state] = {a: 0.0 for a in actions}
    return Q[state]

# -------------------- PARAMETRES NON-LEARNING --------------------
epsilon = 0.0  # plus d'exploration
alpha = 0.0    # plus de mise à jour

# -------------------- JEU --------------------
game = Game(board_size)
state = game.snake.get_state(game.board)
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -------- CHOIX DE L'ACTION (toujours exploitation) --------
    q_values = get_Q(state)
    action = max(q_values, key=q_values.get)

    # -------- STEP DU JEU --------
    next_state, reward, done = game.step(action)
    next_state = game.snake.get_state(game.board)

    # -------- MISE A JOUR Q (alpha=0 donc pas de changement) --------
    best_next_action = max(get_Q(next_state), key=get_Q(next_state).get)
    td_target = reward + 0.9 * get_Q(next_state)[best_next_action]
    td_error = td_target - get_Q(state)[action]
    get_Q(state)[action] += alpha * td_error  # alpha=0 → Q-table figée

    state = next_state

    # -------- AFFICHAGE --------
    screen.fill((0,0,0))

    # Snake
    for x, y in game.snake.segments:
        pygame.draw.rect(screen, (0,0,255),
                         (x*cell_size, y*cell_size, cell_size, cell_size))

    # Pommes vertes
    for green in game.board.green_apples:
        x, y = green.position
        pygame.draw.rect(screen, green.color,
                         (x*cell_size, y*cell_size, cell_size, cell_size))

    # Pomme rouge
    red = game.board.red_apple
    x, y = red.position
    pygame.draw.rect(screen, red.color,
                     (x*cell_size, y*cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(10)  # vitesse du jeu

pygame.quit()
print("Partie terminée ! Mode non-learning.")
