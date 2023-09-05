import pygame
from pygame.locals import *
import random
import winsound
import sys
import time
from screeninfo import get_monitors


# Initialize Pygame
pygame.init()

# Access the main monitor's resolution
for m in get_monitors():
    print(str(m.width))

    if m.is_primary:
        WIDTH = m.width
        HEIGHT = m.height

# Set up the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define game constants
BALL_RADIUS = 30
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 180
BALL_SPEED_X = 8
BALL_SPEED_Y = 8
PADDLE_SPEED = 15

# Set up the scoreboard
score_font = pygame.font.Font(None, 50)
player1_score = 0
player2_score = 0

# Define Powerups
player1_power_up = False
player2_power_up = False
power_up_font = pygame.font.Font(None, 50)
player1_active = False
player2_active = False
power_up_duration = 5000
player1_power_up_end_time = 3000
player2_power_up_end_time = 3000

# Countdown Timer
clock = pygame.time.Clock()
countdown_seconds = 5  # Change this value as per your requirement
player1_remaining_time = countdown_seconds * 1000  # Convert seconds to milliseconds
player2_remaining_time = countdown_seconds * 1000  # Convert seconds to milliseconds

# Create paddles and ball
player_paddle = pygame.Rect(
    50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
)
opponent_paddle = pygame.Rect(
    WIDTH - 50 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
ball = pygame.Rect(
    WIDTH // 2 - BALL_RADIUS // 2,
    HEIGHT // 2 - BALL_RADIUS // 2,
    BALL_RADIUS,
    BALL_RADIUS,
)
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

flicker_timer = 250
flicker_interval = 500  # flicker interval in milliseconds

# Music
paddle_effect = pygame.mixer.Sound("sounds/paddle_effect2.wav")
wall_effect = pygame.mixer.Sound("sounds/wall_effect.mp3")
game_track = pygame.mixer.Sound("sounds/game_track.mp3")
point_effect = pygame.mixer.Sound("sounds/point_effect.wav")

# power_ups = ['Reverse', 'Big', 'Small', 'Power', 'Soft', 'Extra-Life', 'Freeze', 'Flicker-ball']
"""
power_ups = [
    "Laser",
    "Boomer",
    "Sonic",
    "Extra-Life",
]
"""
power_ups = ["Slow"]
# power_ups = ['reverse',  'slow']
#'Inverse' 'Extra-Life',
#'Laser', 'Boomer' 'Sonic'

player1_rumble = None
player2_rumble = None


def reset_game():
    global ball_speed_x, ball_speed_y, player1_power_up, player2_power_up, player1_active, player2_active, player1_remaining_time, player2_remaining_time
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
    ball.x = WIDTH // 2 - BALL_RADIUS // 2
    ball.y = HEIGHT // 2 - BALL_RADIUS // 2
    player1_remaining_time = countdown_seconds * 1000
    player2_remaining_time = countdown_seconds * 1000
    player1_active = False
    player1_power_up = False
    player2_active = False
    player2_power_up = False


def paddle_movement(player1, mod, paddle_speed, inverse):
    global player_paddle, opponent_paddle
    keys = pygame.key.get_pressed()

    if player1:
        player_paddle = pygame.Rect(
            50, player_paddle.y, PADDLE_WIDTH * mod, PADDLE_HEIGHT * mod
        )
        if inverse:
            if keys[pygame.K_w] and player_paddle.y > 0:
                player_paddle.y += paddle_speed
            if keys[pygame.K_s] and player_paddle.y < HEIGHT - PADDLE_HEIGHT * mod:
                player_paddle.y -= paddle_speed
        else:
            if keys[pygame.K_w] and player_paddle.y > 0:
                player_paddle.y -= paddle_speed
            if keys[pygame.K_s] and player_paddle.y < HEIGHT - PADDLE_HEIGHT * mod:
                player_paddle.y += paddle_speed
    else:
        opponent_paddle = pygame.Rect(
            WIDTH - 50 - PADDLE_WIDTH * mod,
            opponent_paddle.y,
            PADDLE_WIDTH * mod,
            PADDLE_HEIGHT * mod,
        )
        if inverse:
            if keys[pygame.K_UP] and opponent_paddle.y > 0:
                opponent_paddle.y += paddle_speed
            if keys[pygame.K_DOWN] and opponent_paddle.y < HEIGHT - PADDLE_HEIGHT * mod:
                opponent_paddle.y -= paddle_speed
        else:
            if keys[pygame.K_UP] and opponent_paddle.y > 0:
                opponent_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and opponent_paddle.y < HEIGHT - PADDLE_HEIGHT * mod:
                opponent_paddle.y += paddle_speed


def ball_movement():
    ball.x += ball_speed_x
    ball.y += ball_speed_y


def paddle_collision(mod):
    global ball_speed_x, ball_speed_y, player1_active, player2_active

    if ball.colliderect(player_paddle):
        pygame.mixer.Sound.play(paddle_effect)
        if player1_active:
            if player1_rumble == "Laser":
                time.sleep(1)
                ball_speed_x *= -5
                ball_speed_y = 0
                player1_active = False
            elif player1_rumble == "Boomer":
                ball_speed_x *= -mod
                ball_speed_y *= mod

            else:
                ball_speed_x *= -1.1
                ball_speed_y *= -1.1
        else:
            ball_speed_x *= -1.1
            ball_speed_y *= 1.1

    if ball.colliderect(opponent_paddle):
        pygame.mixer.Sound.play(paddle_effect)
        if player2_active:
            if player2_rumble == "Laser":
                time.sleep(1)
                ball_speed_x *= -5
                ball_speed_y = 0
                player2_active = False

            elif player2_rumble == "Boomer":
                ball_speed_x *= -mod
                ball_speed_y *= mod

            else:
                ball_speed_x *= -1.1
                ball_speed_y *= 1.1
        else:
            ball_speed_x *= -1.1
            ball_speed_y *= 1.1


def wall_collision():
    global ball_speed_y
    if ball.y > HEIGHT - BALL_RADIUS or ball.y < 0:
        pygame.mixer.Sound.play(wall_effect)
        ball_speed_y *= -1


def score():
    global player1_score, player2_score, player1_active, player2_active
    # Check if ball is missed
    if ball.x > WIDTH:
        if player1_active and player1_rumble == "Extra-Life":
            ball_speed_x * -1.1
            ball_speed_y * -1.1
            player1_active = False
        else:
            # Player missed the ball
            pygame.mixer.Sound.play(point_effect)
            player1_score += 1

            # Reset ball position and direction
            reset_game()

    elif ball.x < 0:
        # Opponent missed the ball
        if player2_active and player2_rumble == "Extra-Life":
            ball_speed_x * -1.1
            ball_speed_y * -1.1
            player2_active = False
        else:
            # Player missed the ball
            pygame.mixer.Sound.play(point_effect)
            player2_score += 1
            # Reset ball position and direction
            reset_game()


pygame.mixer.Sound.play(game_track)


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_r:
                reset_game()
            elif event.key == K_q:
                running = False
            elif event.key == K_z:
                player1_score += 1
            elif event.key == K_m:
                pygame.mixer.stop()

            elif event.key == K_SPACE and player1_power_up:
                player1_active = True
                player1_power_up = False
                player1_power_up_end_time = (
                    pygame.time.get_ticks() + power_up_duration
                )  # Calculate the time when the power-up will end

            elif event.key == K_RCTRL and player2_power_up:
                player2_active = True
                player2_power_up = False
                player2_power_up_end_time = (
                    pygame.time.get_ticks() + power_up_duration
                )  # Calculate the time when the power-up will end

    score()

    if player1_remaining_time <= 0:
        player1_power_up = True  # Activate the power-up effect
        player1_rumble = random.choice(power_ups)
        print(player1_rumble)

    if player2_remaining_time <= 0:
        player2_power_up = True  # Activate the power-up effect
        player2_rumble = random.choice(power_ups)
        print(player2_rumble)

    # Update the countdown
    player1_remaining_time -= clock.tick(120)
    player2_remaining_time -= clock.tick(120)

    if player1_power_up and pygame.time.get_ticks() >= player1_power_up_end_time:
        player1_active = False

        player1_remaining_time = (
            countdown_seconds * 1000
        )  # Reset the remaining time for player 1

    if player2_power_up and pygame.time.get_ticks() >= player2_power_up_end_time:
        player2_active = False

        player2_remaining_time = (
            countdown_seconds * 1000
        )  # Reset the remaining time for player 1

    # Makes paddle big and hit ball harder
    if player1_active:
        if player1_rumble == "Reverse":
            paddle_movement(True, 1, PADDLE_SPEED, False)
            paddle_movement(False, 1, PADDLE_SPEED, True)

        if player1_rumble == "Sonic":
            paddle_movement(True, 1, PADDLE_SPEED, False)
            paddle_movement(False, 1, PADDLE_SPEED * 2, False)

        if player1_rumble == "Boomer":
            paddle_movement(True, 2, PADDLE_SPEED, False)

        if player1_rumble == "Slow":
            paddle_movement(True, 1, PADDLE_SPEED, False)
            paddle_movement(False, 1, PADDLE_SPEED * 0.5, False)

    else:
        paddle_movement(True, 1, PADDLE_SPEED, False)

    if player2_active:
        if player2_rumble == "Reverse":
            paddle_movement(False, 1, PADDLE_SPEED, False)
            paddle_movement(True, 1, PADDLE_SPEED, True)

        if player2_rumble == "Sonic":
            paddle_movement(False, 1, PADDLE_SPEED, False)
            paddle_movement(True, 1, PADDLE_SPEED * 2, False)

        if player2_rumble == "Boomer":
            paddle_movement(False, 2, PADDLE_SPEED, False)

        if player1_rumble == "Slow":
            paddle_movement(False, 1, PADDLE_SPEED, False)
            paddle_movement(True, 1, PADDLE_SPEED * 0.5, False)
    else:
        paddle_movement(False, 1, PADDLE_SPEED, False)

    # Move the ball
    ball_movement()

    # paddle collision physics
    paddle_collision(1.2)

    # Collision detection with walls
    wall_collision()

    # Clear the screen
    WIN.fill(BLACK)

    # Draw the remaining time for player 1 on the screen
    player1_timer_text = power_up_font.render(
        str(player1_remaining_time // 1000), True, WHITE
    )
    player1_ready_text = power_up_font.render(f"Ready! {player1_rumble}", True, WHITE)
    player2_ready_text = power_up_font.render(f"Ready! {player2_rumble}", True, WHITE)
    power_up_text = power_up_font.render(f"{player1_rumble}!", True, WHITE)

    if player1_power_up:
        WIN.blit(
            player1_ready_text,
            (WIDTH // 4 - player1_ready_text.get_width() // 2, 20),
        )
    elif player1_active:
        WIN.blit(power_up_text, (WIDTH // 4 - player1_timer_text.get_width() // 2, 20))
    else:
        WIN.blit(
            player1_timer_text,
            (WIDTH // 4 - player1_timer_text.get_width() // 2, 20),
        )

    # Draw the remaining time for player 2 on the screen
    player2_timer_text = power_up_font.render(
        str(player2_remaining_time // 1000), True, WHITE
    )
    if player2_power_up:
        WIN.blit(
            player2_ready_text,
            (3 * WIDTH // 4 - player2_ready_text.get_width() // 2, 20),
        )
    elif player2_active:
        WIN.blit(
            power_up_text,
            (3 * WIDTH // 4 - player1_timer_text.get_width() // 2, 20),
        )
    else:
        WIN.blit(
            player2_timer_text,
            (3 * WIDTH // 4 - player2_timer_text.get_width() // 2, 20),
        )

    # Draw the scoreboard
    score_text = score_font.render(f"{player1_score} - {player2_score}", True, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    # Draw the paddles and ball
    if player1_rumble == "Boomer" and player1_active:
        pygame.draw.rect(WIN, RED, player_paddle)
    else:
        pygame.draw.rect(WIN, WHITE, player_paddle)

    if player2_rumble == "Boomer" and player2_active:
        pygame.draw.rect(WIN, RED, opponent_paddle)
    else:
        pygame.draw.rect(WIN, WHITE, opponent_paddle)
    """
    if pygame.time.get_ticks() - flicker_timer >= flicker_interval:
        pygame.draw.ellipse(WIN, BLACK, ball)
        flicker_timer = pygame.time.get_ticks()
    else:
        pygame.draw.ellipse(WIN, WHITE, ball)
    """
    pygame.draw.ellipse(WIN, WHITE, ball)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
