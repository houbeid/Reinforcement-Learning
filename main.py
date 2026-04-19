#!/usr/bin/env python3
import pygame
import random
import pickle
import os
import argparse
from game import Game


def main():
    parser = argparse.ArgumentParser(description="Learn2Slither - RL Snake")

    parser.add_argument("-visual", choices=["on", "off"], default="on")
    parser.add_argument("-load", type=str, default=None)
    parser.add_argument("-save", type=str, default=None)
    parser.add_argument("-sessions", type=int, default=None)
    parser.add_argument("-dontlearn", action="store_true")
    parser.add_argument("-step-by-step", action="store_true", dest="step_by_step")

    args = parser.parse_args()

    MODE = "non-learning" if (args.load or args.dontlearn) else "learning"
    RENDER = args.visual == "on"

    TOTAL_EPISODES = args.sessions if args.sessions else (30 if MODE == "non-learning" else 10000)
    cell_size = 40
    board_size = 10

    pygame.init()
    screen = pygame.display.set_mode((cell_size * board_size, cell_size * board_size))
    pygame.display.set_caption("Learn2Slither RL")
    clock = pygame.time.Clock()

    alpha = 0.1
    gamma = 0.9
    epsilon = 1.0
    epsilon_decay = 0.9995
    epsilon_min = 0.01
    MAX_STEPS = 500


    game = Game(board_size)
    Q = {}

    total_rewards = []
    max_length = 0
    max_duration = 0

    actions = ["UP", "DOWN", "LEFT", "RIGHT"]


    if args.load:
        if os.path.exists(args.load):
            with open(args.load, "rb") as f:
                Q = pickle.load(f)
            epsilon = 0
            print(f"Load trained model from {args.load}")
        else:
            print("Model not found")
            return


    def choose_action(state):
        nonlocal epsilon

        if MODE == "learning" and random.random() < epsilon:
            return random.choice(actions)

        if state not in Q:
            Q[state] = {a: 0 for a in actions}

        return max(Q[state], key=Q[state].get)

    def update_q(state, action, reward, next_state):
        if state not in Q:
            Q[state] = {a: 0 for a in actions}
        if next_state not in Q:
            Q[next_state] = {a: 0 for a in actions}

        td_target = reward + gamma * max(Q[next_state].values())
        td_error = td_target - Q[state][action]
        Q[state][action] += alpha * td_error


    for episode in range(TOTAL_EPISODES):

        game.reset()
        state = game.snake.get_state(game.board)

        done = False
        steps = 0
        total_reward = 0

        while not done and steps < MAX_STEPS:
            steps += 1

            action = choose_action(state)
            next_state, reward, done = game.step(action)

            total_reward += reward

            if MODE == "learning":
                update_q(state, action, reward, next_state)

            state = next_state


            if RENDER:
                screen.fill((0, 0, 0))

                for x, y in game.snake.segments:
                    pygame.draw.rect(screen, (0, 0, 255),
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                for g in game.board.green_apples:
                    x, y = g.position
                    pygame.draw.rect(screen, g.color,
                                     (x * cell_size, y * cell_size, cell_size, cell_size))

                r = game.board.red_apple
                x, y = r.position
                pygame.draw.rect(screen, r.color,
                                 (x * cell_size, y * cell_size, cell_size, cell_size))

                pygame.display.flip()
                clock.tick(10)

                if args.step_by_step:
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                waiting = False
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            current_len = len(game.snake.segments)
            max_length = max(max_length, current_len)
            max_duration = max(max_duration, steps)

        total_rewards.append(total_reward)

        if MODE == "learning":
            epsilon = max(epsilon_min, epsilon * epsilon_decay)

        if episode % 100 == 0:
            print(f"Episode {episode} | reward={total_reward:.1f} | steps={steps} | len={len(game.snake.segments)}")

        if args.save and episode in [1, 10, 100, 1000, 5000]:
            os.makedirs(args.save, exist_ok=True)
            path = os.path.join(args.save, f"{episode}sess.txt")
            with open(path, "wb") as f:
                pickle.dump(Q, f)
            print("Saved:", path)

    print("\nGame over")
    print(f"max length = {max_length}, max duration = {max_duration}")

    if total_rewards:
        print(f"Score moyen : {sum(total_rewards)/len(total_rewards):.1f}")
        print(f"Score max   : {max(total_rewards):.1f}")
        print(f"Score min   : {min(total_rewards):.1f}")

    pygame.quit()

if __name__ == "__main__":
    main()