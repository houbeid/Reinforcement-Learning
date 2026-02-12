# main.py
import pygame
from game import Game

pygame.init()

cell_size = 40
board_size = 10
screen = pygame.display.set_mode((cell_size*board_size, cell_size*board_size))
pygame.display.set_caption("Learn2Slither RL")
clock = pygame.time.Clock()

# Création du jeu
game = Game(board_size)

running = True
action = "RIGHT"  # direction initiale

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = "UP"
            elif event.key == pygame.K_DOWN:
                action = "DOWN"
            elif event.key == pygame.K_LEFT:
                action = "LEFT"
            elif event.key == pygame.K_RIGHT:
                action = "RIGHT"

    # Mettre à jour la direction et bouger
    game.snake.update_direction(action)
    state, reward, done = game.step(action)

    if done:
        print("Game Over!")
        running = False

    # Dessiner le board
    screen.fill((0,0,0))
    # Snake
    for x, y in game.snake.segments:
        pygame.draw.rect(screen, (0,0,255), (x*cell_size, y*cell_size, cell_size, cell_size))
    # Pommes vertes
    for green in game.board.green_apples:
        x, y = green.position
        pygame.draw.rect(screen, green.color, (x*cell_size, y*cell_size, cell_size, cell_size))
    # Pomme rouge
    red = game.board.red_apple
    x, y = red.position
    pygame.draw.rect(screen, red.color, (x*cell_size, y*cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(5)  # vitesse du jeu (5 FPS)

pygame.quit()
