import pygame
from pygame.locals import *
import sys

# Game constants
window_width = 640
window_height = 480
paddle_width = 10
paddle_height = 60
paddle_speed = 5
ball_radius = 5
ball_speed_x = 3
ball_speed_y = 3
score_limit = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(window_width/2, window_height/2))
    window.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

    reset_game()

def reset_game():
    global player_score, ai_score, player_paddle, ai_paddle, ball

    player_score = 0
    ai_score = 0

    player_paddle = pygame.Rect(10, window_height / 2 - paddle_height / 2, paddle_width, paddle_height)
    ai_paddle = pygame.Rect(window_width - paddle_width - 10, window_height / 2 - paddle_height / 2, paddle_width, paddle_height)
    ball = pygame.Rect(window_width / 2 - ball_radius, window_height / 2 - ball_radius, ball_radius * 2, ball_radius * 2)

def update_score():
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(str(player_score), True, WHITE)
    ai_score_text = font.render(str(ai_score), True, WHITE)
    player_score_rect = player_score_text.get_rect(left=window_width/2 - 50, top=10)
    ai_score_rect = ai_score_text.get_rect(right=window_width/2 + 50, top=10)
    window.blit(player_score_text, player_score_rect)
    window.blit(ai_score_text, ai_score_rect)

def check_game_over():
    if player_score >= score_limit or ai_score >= score_limit:
        show_game_over_screen()

# Initialize the game
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

# Game state variables
player_score = 0
ai_score = 0

player_paddle = pygame.Rect(10, window_height / 2 - paddle_height / 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(window_width - paddle_width - 10, window_height / 2 - paddle_height / 2, paddle_width, paddle_height)
ball = pygame.Rect(window_width / 2 - ball_radius, window_height / 2 - ball_radius, ball_radius * 2, ball_radius * 2)

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if player_score >= score_limit or ai_score >= score_limit:
                    reset_game()

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[K_w] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[K_s] and player_paddle.bottom < window_height:
        player_paddle.y += paddle_speed

    # Move the AI paddle
    if ball.top < ai_paddle.top and ai_paddle.top > 0:
        ai_paddle.y -= paddle_speed
    if ball.bottom > ai_paddle.bottom and ai_paddle.bottom < window_height:
        ai_paddle.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Check collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x *= -1

    # Check collision with walls
    if ball.top < 0 or ball.bottom > window_height:
        ball_speed_y *= -1

    # Check if ball went out of bounds
    if ball.left < 0:
        ai_score += 1
        check_game_over()
        ball.center = (window_width / 2, window_height / 2)
    if ball.right > window_width:
        player_score += 1
        check_game_over()
        ball.center = (window_width / 2, window_height / 2)

    # Draw the game objects
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, player_paddle)
    pygame.draw.rect(window, WHITE, ai_paddle)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (window_width / 2, 0), (window_width / 2, window_height))

    update_score()

    pygame.display.update()
    clock.tick(60)
