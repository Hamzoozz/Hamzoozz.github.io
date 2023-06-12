import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
width = 640
height = 640
game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set up colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the snake and food
snake_pos = [(width // 2, height // 2)]
snake_size = 20
food_pos = (random.randint(0, width - snake_size) // snake_size * snake_size,
            random.randint(0, height - snake_size) // snake_size * snake_size)
food_size = 20
direction = 'RIGHT'

# Set up the game over flag
game_over = False

# Set up the score
score = 0

# Set up the font
font = pygame.font.Font(None, 36)

def display_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    game_window.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    game_window.blit(game_over_text, (width // 2 - 80, height // 2 - 20))

    retry_text = font.render("Retry", True, WHITE)
    pygame.draw.rect(game_window, GREEN, pygame.Rect(width // 2 - 40, height // 2 + 20, 80, 40))
    game_window.blit(retry_text, (width // 2 - 25, height // 2 + 30))

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if width // 2 - 40 <= mouse_pos[0] <= width // 2 + 40 and height // 2 + 20 <= mouse_pos[1] <= height // 2 + 60:
                if game_over:
                    # Reset game
                    snake_pos = [(width // 2, height // 2)]
                    direction = 'RIGHT'
                    score = 0
                    game_over = False

    # Update snake position
    if direction == 'UP':
        new_head = (snake_pos[0][0], snake_pos[0][1] - snake_size)
    elif direction == 'DOWN':
        new_head = (snake_pos[0][0], snake_pos[0][1] + snake_size)
    elif direction == 'LEFT':
        new_head = (snake_pos[0][0] - snake_size, snake_pos[0][1])
    else:
        new_head = (snake_pos[0][0] + snake_size, snake_pos[0][1])
    snake_pos.insert(0, new_head)

    # Check for collision with food
    if snake_pos[0] == food_pos:
        score += 100
        food_pos = (random.randint(0, width - snake_size) // snake_size * snake_size,
                    random.randint(0, height - snake_size) // snake_size * snake_size)
    else:
        snake_pos.pop()

    # Check for collision with the walls
    if (snake_pos[0][0] < 0 or snake_pos[0][0] >= width or
            snake_pos[0][1] < 0 or snake_pos[0][1] >= height):
        game_over = True

    # Check for collision with the snake itself
    if snake_pos[0] in snake_pos[1:]:
        game_over = True

    # Clear the game window
    game_window.fill(BLACK)

    # Draw the snake
    for pos in snake_pos:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    # Draw the food
    pygame.draw.rect(game_window, RED, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

    # Display the score
    display_score()

    if game_over:
        display_game_over()

    # Update the game window
    pygame.display.flip()

    # Set the game speed
    clock.tick(10)

# Quit the game
pygame.quit()


