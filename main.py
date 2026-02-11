import pygame
from snake import Snake
from Apple import Apple


pygame.init()
cell_size = 40
board_size = 10
screen = pygame.display.set_mode((cell_size*board_size, cell_size*board_size))
clock = pygame.time.Clock()
snake = Snake(start_pos=(5,5), initial_length=3)
green1 = Apple(board_size, color=(0,255,0))
green2 = Apple(board_size, color=(0,255,0))
red = Apple(board_size, color=(255,0,0))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    # Mettre à jour le Snake
    snake.move()
    if snake.check_wall_collision(board_size):
        print("Game Over: Snake hit the wall!")
        running = False
    for green in [green1, green2]:
        if snake.head() == green.position:
            snake.grow()  # grandir
            # réinitialiser la pomme à une nouvelle position
            green.respawn(snake.segments, other_apples=[green1.position, green2.position, red.position])
        if snake.head() == red.position:
            if len(snake.segments) > 1:
                snake.segments.pop()  # rétrécit
            else:
                print("Game Over: Snake too short!")
                running = False  # fin du jeu
            red.respawn(snake.segments, other_apples=[green1.position, green2.position])
    screen.fill((0,0,0))  # noir pour le fond

    # Dessiner snake
    for x, y in snake.segments:  # <- segments au lieu de snake
        pygame.draw.rect(screen, (0,0,255), (x*cell_size, y*cell_size, cell_size, cell_size))
    for apple in [green1, green2, red]:
        x, y = apple.position
        pygame.draw.rect(screen, apple.color, (x*cell_size, y*cell_size, cell_size, cell_size))

    pygame.display.flip()
    clock.tick(5)  # vitesse de l'affichage
pygame.quit()