import pygame
import random
import pickle
import os
import argparse
from game import Game

# ================= Arguments CLI =================
# Usage exemples :
#   ./snake -visual on -load models/1000sess.txt
#   ./snake -visual off -sessions 10000 -save models/
#   ./snake -visual on -sessions 100

parser = argparse.ArgumentParser(description="Learn2Slither - RL Snake")

parser.add_argument("-visual",   choices=["on", "off"], default="on",
                    help="Afficher le jeu (on) ou apprentissage rapide (off)")
parser.add_argument("-load",     type=str, default=None,
                    help="Charger un modèle existant (ex: models/1000sess.txt)")
parser.add_argument("-save",     type=str, default=None,
                    help="Dossier de sauvegarde des modèles (ex: models/)")
parser.add_argument("-sessions", type=int, default=None,
                    help="Nombre d'épisodes (défaut: 100 si -load, 10000 sinon)")
parser.add_argument("-dontlearn", action="store_true",
                    help="Ne pas mettre à jour la Q-table (évaluation pure)")
parser.add_argument("-step-by-step", action="store_true", dest="step_by_step",
                    help="Avancer étape par étape (appuyer sur une touche)")

args = parser.parse_args()

# ================= Déduction du mode =================
MODE = "non-learning" if (args.load or args.dontlearn) else "learning"
RENDER = args.visual == "on"

# Nombre d'épisodes selon le mode si non spécifié
if args.sessions is not None:
    TOTAL_EPISODES = args.sessions
else:
    TOTAL_EPISODES = 30 if MODE == "non-learning" else 10000

# ================= Paramètres du board =================
cell_size  = 40
board_size = 10

pygame.init()
screen = pygame.display.set_mode((cell_size * board_size, cell_size * board_size))
pygame.display.set_caption("Learn2Slither RL")
clock = pygame.time.Clock()

# ================= Q-learning parameters =================
alpha         = 0.1
gamma         = 0.9
epsilon       = 1.0
epsilon_decay = 0.9995
epsilon_min   = 0.01
MAX_STEPS     = 500

SAVE_EPISODES = [1, 10, 100, 500, 1000, 5000, 10000, 50000]

# ================= Initialisation =================
game          = Game(board_size)
Q             = {}
total_rewards = []
max_length    = 0
max_duration  = 0

# ================= Fonctions =================
def choose_action(state):
    global epsilon
    actions = ["UP", "DOWN", "LEFT", "RIGHT"]
    if MODE == "learning" and random.random() < epsilon:
        return random.choice(actions)
    else:
        if state not in Q:
            Q[state] = {a: 0 for a in actions}
        return max(Q[state], key=Q[state].get)

def update_q_table(state, action, reward, next_state):
    actions = ["UP", "DOWN", "LEFT", "RIGHT"]
    if state not in Q:
        Q[state] = {a: 0 for a in actions}
    if next_state not in Q:
        Q[next_state] = {a: 0 for a in actions}
    td_target        = reward + gamma * max(Q[next_state].values())
    td_error         = td_target - Q[state][action]
    Q[state][action] += alpha * td_error

def save_model(episode):
    """Sauvegarde la Q-table au format texte."""
    folder = args.save if args.save else "."
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{episode}sess.txt")
    with open(filename, "wb") as f:
        pickle.dump(Q, f)
    print(f"  --> Modèle sauvegardé : {filename}")

# ================= Charger modèle =================
if args.load:
    if os.path.exists(args.load):
        with open(args.load, "rb") as f:
            Q = pickle.load(f)
        epsilon = 0
        print(f"Load trained model from {args.load}")
        print(f"Evaluation sur {TOTAL_EPISODES} épisodes...\n")
    else:
        print(f"Erreur : fichier '{args.load}' introuvable.")
        exit(1)

# ================= Boucle principale =================
for episode in range(1, TOTAL_EPISODES + 1):
    game.reset()
    state        = game.snake.get_state(game.board)
    done         = False
    steps        = 0
    total_reward = 0

    while not done and steps < MAX_STEPS:
        steps += 1

        action                  = choose_action(state)
        next_state, reward, done = game.step(action)
        total_reward            += reward

        if MODE == "learning":
            update_q_table(state, action, reward, next_state)

        state = next_state

        # Suivi max length / max duration
        current_length = len(game.snake.segments)
        if current_length > max_length:
            max_length = current_length
        if steps > max_duration:
            max_duration = steps

        if RENDER:
            screen.fill((0, 0, 0))
            for x, y in game.snake.segments:
                pygame.draw.rect(screen, (0, 0, 255),
                                 (x * cell_size, y * cell_size, cell_size, cell_size))
            for green in game.board.green_apples:
                x, y = green.position
                pygame.draw.rect(screen, green.color,
                                 (x * cell_size, y * cell_size, cell_size, cell_size))
            red  = game.board.red_apple
            x, y = red.position
            pygame.draw.rect(screen, red.color,
                             (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.display.flip()
            if args.step_by_step:
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            waiting = False
            clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    # ================= Fin d'épisode =================
    total_rewards.append(total_reward)

    if MODE == "learning":
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        if episode in SAVE_EPISODES:
            print(f"Episode {episode:>6} | epsilon={epsilon:.4f} | "
                  f"reward={total_reward:>7.1f} | steps={steps:>4} | "
                  f"length={len(game.snake.segments)}")
            if args.save:
                save_model(episode)

        elif episode % 500 == 0:
            print(f"Episode {episode:>6} | epsilon={epsilon:.4f} | "
                  f"reward={total_reward:>7.1f} | steps={steps:>4} | "
                  f"length={len(game.snake.segments)}")

    elif MODE == "non-learning":
        print(f"Episode {episode:>4} | reward={total_reward:>7.1f} | "
              f"steps={steps:>4} | length={len(game.snake.segments)}")

# ================= Bilan final =================
print(f"\nGame over, max length = {max_length}, max duration = {max_duration}")

if len(total_rewards) > 0:
    print(f"Score moyen : {sum(total_rewards) / len(total_rewards):.1f}")
    print(f"Score max   : {max(total_rewards):.1f}")
    print(f"Score min   : {min(total_rewards):.1f}")

pygame.quit()