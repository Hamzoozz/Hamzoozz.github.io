import pygame
import random


# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 288, 512  # 288, 512
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Load images
background_img = pygame.image.load("background.png").convert()
bird_img = pygame.image.load("bird.png").convert_alpha()
pipe_img = pygame.image.load("pipe.png").convert_alpha()
game_over_img = pygame.image.load("game_over.png").convert_alpha()
retry_img = pygame.image.load("retry.png").convert_alpha()
start_button_img = pygame.image.load("start_button.png").convert_alpha()
auto_play_button_img = pygame.image.load("auto_play_button.png").convert_alpha()

# Scale images to the desired sizes
bird_img = pygame.transform.scale(bird_img, (50, 50))  
pipe_img = pygame.transform.scale(pipe_img, (70, 500)) # 70,200
game_over_img = pygame.transform.scale(game_over_img, (200, 100)) # 200,100
retry_img = pygame.transform.scale(retry_img, (100, 50))
start_button_img = pygame.transform.scale(start_button_img, (100, 50))
auto_play_button_img = pygame.transform.scale(auto_play_button_img, (100, 50))
background_img = pygame.transform.scale(background_img, (288, 512))

# Load sound effects
flap_sound = pygame.mixer.Sound("flap.wav")
collision_sound = pygame.mixer.Sound("collision.wav") 
point_sound = pygame.mixer.Sound("point.wav")

# Game variables
clock = pygame.time.Clock()
gravity = 0.5
jump_power = -8.5 #-10
bird_movement = 0
score = 0
game_font = pygame.font.Font("04B_19.ttf", 40)
outline_font = pygame.font.Font("04B_19.ttf", 42)
outline_font.set_bold(True)

# Define the bird class
class Bird:

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self):
        self.x = 50
        self.y = 256
        self.movement = 0
        self.img_count = 0
        self.img = bird_img

    def jump(self):
        self.movement = jump_power
        flap_sound.play()

    def update(self):
        self.movement += gravity
        self.y += self.movement

    def draw(self, win):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = bird_img
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = bird_img  # Replace with the second image
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = bird_img  # Replace with the third image
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = bird_img  # Replace with the second image
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = bird_img
            self.img_count = 0

        # Rotate the bird
        rotated_image = pygame.transform.rotate(self.img, self.movement * -6) # -3
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

# Define the pipe class
class Pipe:
    def __init__(self):
        self.x = 300
        self.gap = 150
        self.height = random.randint(20, 300) # 50, 300 / 100, 300
        self.passed = False

    def update(self):
        self.x -= 3

    def collision(self, bird_rect):
        if bird_rect.colliderect(self.upper_rect) or bird_rect.colliderect(self.lower_rect):
            return True
        return False

    def draw(self, win):
        self.upper_rect = pygame.Rect(self.x, 0, pipe_img.get_width(), self.height)
        self.lower_rect = pygame.Rect(self.x, self.height + self.gap, pipe_img.get_width(), height - self.height - self.gap)
        win.blit(pipe_img, (self.x, self.height - pipe_img.get_height()))
        win.blit(pygame.transform.flip(pipe_img, False, True), (self.x, self.height + self.gap))

    def off_screen(self):
        return self.x < -pipe_img.get_width()

# Initialize the bird and pipe objects
bird = Bird()
pipes = [Pipe()]

game_over = False
game_started = False
auto_play = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_started and not game_over:
                    bird.jump()
                elif game_over:
                    # Restart the game
                    game_over = False
                    bird = Bird()
                    pipes = [Pipe()]
                    score = 0
            elif event.key == pygame.K_a:
                auto_play = not auto_play

    window.blit(background_img, (0, 0))

    if not game_started:
        # Draw start button
        start_button_rect = pygame.Rect(width // 2 - start_button_img.get_width() // 2, height // 2 - 50, start_button_img.get_width(), start_button_img.get_height())
        window.blit(start_button_img, (start_button_rect.x, start_button_rect.y))

        # Check for start button click
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(mouse_pos):
            game_started = True

    elif not game_over:
        # Update and draw the bird
        bird.update()
        bird.draw(window)

        # Update and draw the pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw(window)

            # Check for collision with pipes
            if pipe.collision(pygame.Rect(bird.x, bird.y, bird_img.get_width(), bird_img.get_height())) or bird.y > height:
                collision_sound.play()
                game_over = True

            if not auto_play:
                # Check for collision with the top barrier
                if bird.y <= 0:
                    collision_sound.play()
                    game_over = True

            if bird.x > pipe.x + pipe_img.get_width() and not pipe.passed:
                pipe.passed = True
                score += 1
                point_sound.play()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Add new pipes
        if len(pipes) < 5 and pipes[-1].x < width - 200:
            pipes.append(Pipe())

        if auto_play:
            bird.jump()

        # Draw the score
        score_text = game_font.render(str(score), True, (255, 255, 255))
        score_text_outline = outline_font.render(str(score), True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(width // 2, 50))
        score_rect_outline = score_text_outline.get_rect(center=(width // 2, 50))

        window.blit(score_text_outline, score_rect_outline.move(2, 2))
        window.blit(score_text_outline, score_rect_outline.move(-2, -2))
        window.blit(score_text_outline, score_rect_outline.move(2, -2))
        window.blit(score_text_outline, score_rect_outline.move(-2, 2))
        window.blit(score_text, score_rect)

    else:
        # Draw game over image
        window.blit(game_over_img, (width // 2 - game_over_img.get_width() // 2, height // 2 - game_over_img.get_height()))

        # Draw retry image
        retry_rect = pygame.Rect(width // 2 - retry_img.get_width() // 2, height // 2 + 20, retry_img.get_width(), retry_img.get_height())
        window.blit(retry_img, (retry_rect.x, retry_rect.y))

        # Check for retry button click
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and retry_rect.collidepoint(mouse_pos):
            game_over = False
            bird = Bird()
            pipes = [Pipe()]
            score = 0

# Draw auto play button
    auto_play_button_rect = pygame.Rect(width - auto_play_button_img.get_width() - 10, height - auto_play_button_img.get_height() - 10, auto_play_button_img.get_width(), auto_play_button_img.get_height())
    if auto_play:
        pygame.draw.rect(window, (0, 255, 0), auto_play_button_rect, border_radius=5)
    else:
        pygame.draw.rect(window, (255, 0, 0), auto_play_button_rect, border_radius=5)
    window.blit(auto_play_button_img, (auto_play_button_rect.x, auto_play_button_rect.y))

    # Check for auto play button click
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] and auto_play_button_rect.collidepoint(mouse_pos):
        auto_play = not auto_play

    # Display the final score at the top
    if game_over:
        final_score_text = game_font.render("Score: " + str(score), True, (255, 255, 255))
        final_score_text_outline = outline_font.render("Score: " + str(score), True, (0, 0, 0))
        final_score_rect = final_score_text.get_rect(center=(width // 2, 50))
        final_score_rect_outline = final_score_text_outline.get_rect(center=(width // 2, 50))

        window.blit(final_score_text_outline, final_score_rect_outline.move(2, 2))
        window.blit(final_score_text_outline, final_score_rect_outline.move(-2, -2))
        window.blit(final_score_text_outline, final_score_rect_outline.move(2, -2))
        window.blit(final_score_text_outline, final_score_rect_outline.move(-2, 2))
        window.blit(final_score_text, final_score_rect)



    pygame.display.update()
    clock.tick(60)

pygame.quit()
