import pygame, sys
from button import Button
from pygame.locals import *
import random
import time
from screeninfo import get_monitors

# Initialize Pygame
pygame.init()

# Access the main monitor's resolution
for m in get_monitors():
    if m.is_primary:
        WIDTH = m.width
        HEIGHT = m.height

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"assets\font.ttf", size)


# Pause menu
pause = False
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Set up the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BCKGD = (44, 2, 28, 255)

# Define game constants
BALL_RADIUS = 30
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 180
BALL_SPEED_X = 8
BALL_SPEED_Y = 8
PADDLE_SPEED = 15

# Set up the scoreboard
score_font = pygame.font.Font(None, 100)
player1_score = 0
player2_score = 0
singleplayer_score = 0
mode = None

# Define Powerups
player1_power_up = False
player2_power_up = False
power_up_font = pygame.font.Font(None, 50)
player1_active = False
player2_active = False
power_up_duration = 5000
player1_power_up_end_time = 3000
player2_power_up_end_time = 3000
highscore = 0

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
ball_speed_y = BALL_SPEED_Y * random.uniform(-3, 3)


# Dealing with sound
music_option = ""
music_enabled = True
sound_effect_option = ""
sound_effect_enabled = True

# Music
paddle_effect = pygame.mixer.Sound("sounds/paddle_effect2.wav")
wall_effect = pygame.mixer.Sound("sounds/wall_effect.mp3")
point_effect = pygame.mixer.Sound("sounds/point_effect.wav")
laser_effect = pygame.mixer.Sound("sounds/laser_effect.mp3 ")
button_effect = pygame.mixer.Sound("sounds/button_effect.mp3 ")
game_track = "sounds/game_track.mp3"
jazz_menu_track = "sounds/jazz_menu_track.mp3"
main_menu_track = "sounds/main_menu_track.mp3"

# power_ups = ['Reverse', 'Big', 'Small', 'Power', 'Soft', 'Extra-Life', 'Freeze', 'Flicker-ball']
"""
power_ups = [
    "Laser",
    "Boomer",
    "Sonic",
    "Extra-Life",
]
"""
power_ups = ["Boomer", "Sonic", "Laser"]
# power_ups = ['Inverse',  'slow', 'Extra-Life']


player1_rumble = None
player2_rumble = None


def draw_pause():
    global pause
    pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])
    SCREEN.blit(surface, (0, 0))

    PAUSE_MENU_POS = pygame.mouse.get_pos()

    MAIN_MENU_BUTTON = Button(
        image=pygame.image.load(r"assets\Options Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.4),
        text_input="Main Menu",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    RESUME_BUTTON = Button(
        image=pygame.image.load(r"assets\Options Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.5),
        text_input="Resume",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    QUIT_BUTTON = Button(
        image=pygame.image.load(r"assets\Quit Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.8),
        text_input="QUIT",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    for button in [
        MAIN_MENU_BUTTON,
        RESUME_BUTTON,
        QUIT_BUTTON,
    ]:
        button.changeColor(PAUSE_MENU_POS)
        button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MAIN_MENU_BUTTON.checkForInput(PAUSE_MENU_POS):
                sound("button")
                menu()
            elif RESUME_BUTTON.checkForInput(PAUSE_MENU_POS):
                sound("button")
                pause = False
                sound("unpause")
            elif QUIT_BUTTON.checkForInput(PAUSE_MENU_POS):
                sound("button")
                pygame.quit()
                sys.exit()


def game_over():
    global highscore, singleplayer_score
    SCREEN.fill(BLACK)

    GAME_OVER_POS = pygame.mouse.get_pos()

    # Draw the remaining time for player 1 on the screen
    new_high_score_text = get_font(40).render((f"NEW HIGHSCORE!"), True, WHITE)
    
    score_text = get_font(40).render((f"SCORE: {singleplayer_score}"), True, WHITE)

    if singleplayer_score >= highscore:
        
        WIN.blit(
            new_high_score_text,
            (WIDTH / 2 - (new_high_score_text.get_width() / 2), HEIGHT * 0.3),
        )
    
    

    # Draw the remaining time for player 1 on the screen
    game_over_text = get_font(100).render(("GAME OVER"), True, WHITE)

    # Draw the remaining time for player 1 on the screen
    high_score_text = get_font(40).render((f"HIGHSCORE: {highscore}"), True, WHITE)

    WIN.blit(
        game_over_text, (WIDTH / 2 - (game_over_text.get_width() / 2), HEIGHT * 0.2)
    )

    WIN.blit(
        high_score_text, (WIDTH // 2 - (high_score_text.get_width() / 2), HEIGHT * 0.4)
    )
    
    WIN.blit(
            score_text,
            (WIDTH / 2 - (score_text.get_width() / 2), HEIGHT * 0.5),
        )

    MAIN_MENU_BUTTON = Button(
        image=pygame.image.load(r"assets\Options Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.7),
        text_input="Main Menu",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    RESTART_BUTTON = Button(
        image=pygame.image.load(r"assets\Options Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.6),
        text_input="Restart",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    QUIT_BUTTON = Button(
        image=pygame.image.load(r"assets\Quit Rect.png"),
        pos=(WIDTH / 2, HEIGHT * 0.8),
        text_input="QUIT",
        font=get_font(60),
        base_color="White",
        hovering_color="#d7fcd4",
    )

    for button in [
        MAIN_MENU_BUTTON,
        RESTART_BUTTON,
        QUIT_BUTTON,
    ]:
        button.changeColor(GAME_OVER_POS)
        button.update(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if MAIN_MENU_BUTTON.checkForInput(GAME_OVER_POS):
                sound("button")

                menu()
            elif RESTART_BUTTON.checkForInput(GAME_OVER_POS):
                sound("button")
                reset_game()
            elif QUIT_BUTTON.checkForInput(GAME_OVER_POS):
                sound("button")
                pygame.quit()
                sys.exit()


def reset_game():
    global ball_speed_x, ball_speed_y, player1_power_up, player2_power_up, player1_active, player2_active, player1_remaining_time, player2_remaining_time, pause, singleplayer_score
    ball_speed_x = BALL_SPEED_X * random.choice((-1, 1))
    ball_speed_y = BALL_SPEED_Y * random.uniform(-1, 1)
    ball.x = WIDTH // 2 - BALL_RADIUS // 2
    ball.y = HEIGHT // 2 - BALL_RADIUS // 2
    player1_remaining_time = countdown_seconds * 1000
    player2_remaining_time = countdown_seconds * 1000
    player1_active = False
    player1_power_up = False
    player2_active = False
    player2_power_up = False
    pause = False
    singleplayer_score = 0


def paddle_movement(player1, mod, paddle_speed, inverse):
    global player_paddle, opponent_paddle
    keys = pygame.key.get_pressed()

    if player1:
        player_paddle = pygame.Rect(
            50, player_paddle.y, PADDLE_WIDTH * mod, PADDLE_HEIGHT * mod
        )
        if inverse:
            if keys[pygame.K_w] and player_paddle.y < 0:
                player_paddle.y += paddle_speed
            if keys[pygame.K_s] and player_paddle.y > HEIGHT - PADDLE_HEIGHT * mod:
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
    global ball_speed_x, ball_speed_y, player1_active, player2_active, singleplayer_score, highscore

    if ball.colliderect(player_paddle):
        sound("paddle")
        
        
        singleplayer_score += 1
        if singleplayer_score > highscore:
            highscore = singleplayer_score
        

        if player1_active:
            if player1_rumble == "Laser":
                sound("laser")
                time.sleep(1)
                ball_speed_x *= -5
                ball_speed_y = random.uniform(-3, 3)
                player1_active = False
            elif player1_rumble == "Boomer":
                ball_speed_x *= -mod
                ball_speed_y *= mod

            else:
                ball_speed_x *= -1.1
                ball_speed_y *= -1.1
        else:
            ball_speed_x *= -1.1
            ball_speed_y *= random.uniform(-3, 3)

    if ball.colliderect(opponent_paddle):
        sound("paddle")
        if player2_active:
            if player2_rumble == "Laser":
                sound("laser")
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
            ball_speed_y *= random.uniform(-3, 3)


def wall_collision():
    global ball_speed_y
    if ball.y > HEIGHT - BALL_RADIUS or ball.y < 0:
        sound("wall")
        ball_speed_y *= -1


def score(multiplayer):
    global player1_score, player2_score, player1_active, player2_active, ball_speed_x, ball_speed_y

    # Check if ball is missed

    if multiplayer:
        if ball.x > WIDTH:
            # Opponent missed the ball
            sound("point")
            player1_score += 1

            # Reset ball position and direction
            reset_game()

        if ball.x < 0:
            # Player missed the ball
            sound("point")
            player2_score += 1
            # Reset ball position and direction
            reset_game()

    else:
        if ball.x > WIDTH:
            # Opponent missed the ball
            sound("wall")
            ball_speed_x *= -1.1
            ball_speed_y = random.uniform(-3, 3)

        if ball.x < 0:
            # Player missed the ball
            sound("point")
            reset_game()
            # Reset ball position and direction


def singleplayer():
    global pause, music_enabled, sound_effect_enabled, player1_remaining_time, player1_power_up, player1_active, player1_rumble, player1_score, player1_power_up_end_time, player1_remaining_time_display

    pygame.mixer.stop()
    sound("game_track")
    reset_game()
    singleplayer_score = 0

    # Game loop
    running = True
    while running:
        # Handle events
        if pause:
            game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                elif event.key == K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == K_z:
                    player1_score += 1

                elif event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                        sound("unpause")
                    else:
                        pause = True
                        sound("pause")

                elif event.key == K_SPACE and player1_power_up:
                    player1_active = True
                    player1_power_up = False
                    player1_power_up_end_time = (
                        pygame.time.get_ticks() + power_up_duration
                    )  # Calculate the time when the power-up will end

        if not pause:
            score(False)

            if player1_remaining_time <= 0:
                player1_power_up = True  # Activate the power-up effect
                player1_rumble = random.choice(power_ups)
                print(player1_rumble)

            # Update the countdown
            player1_remaining_time -= clock.tick(120)

            if (
                player1_power_up
                and pygame.time.get_ticks() >= player1_power_up_end_time
            ):
                player1_active = False

                player1_remaining_time = (
                    countdown_seconds * 1000
                )  # Reset the remaining time for player 1

            # Makes paddle big and hit ball harder
            if player1_active:
                if player1_rumble == "Inverse":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    paddle_movement(False, 1, PADDLE_SPEED, True)

                if player1_rumble == "Sonic":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    if player2_rumble == "Boomer" and player2_active:
                        paddle_movement(False, 2, PADDLE_SPEED * 2, False)
                    else:
                        paddle_movement(False, 1, PADDLE_SPEED * 2, False)

                if player1_rumble == "Boomer":
                    paddle_movement(True, 2, PADDLE_SPEED, False)

                if player1_rumble == "Slow":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    paddle_movement(False, 2, -1, False)

            else:
                paddle_movement(True, 1, PADDLE_SPEED, False)

            # Move the ball
            ball_movement()

            # paddle collision physics
            paddle_collision(1.2)

            # Collision detection with walls
            wall_collision()

            # Clear the screen
            WIN.fill(BLACK)

            player1_remaining_time_display = round(
                float(player1_remaining_time / 1000), 2
            )

        # Draw the remaining time for player 1 on the screen
        player1_timer_text = power_up_font.render(
            str(player1_remaining_time_display), True, WHITE
        )
        player1_ready_text = power_up_font.render(
            f"Ready! {player1_rumble}", True, WHITE
        )

        power_up_text = power_up_font.render(f"{player1_rumble}!", True, WHITE)

        if player1_power_up:
            WIN.blit(
                player1_ready_text,
                (WIDTH // 4 - player1_ready_text.get_width() // 2, 20),
            )
        elif player1_active:
            WIN.blit(
                power_up_text, (WIDTH // 4 - player1_timer_text.get_width() // 2, 20)
            )
        else:
            WIN.blit(
                player1_timer_text,
                (WIDTH // 4 - player1_timer_text.get_width() // 2, 20),
            )

        # Draw the scoreboard
        score_text = get_font(50).render(f"{singleplayer_score}", True, WHITE)
        WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Draw the paddles and ball
        if player1_rumble == "Boomer" and player1_active:
            pygame.draw.rect(WIN, RED, player_paddle)
        else:
            pygame.draw.rect(WIN, WHITE, player_paddle)

        pygame.draw.ellipse(WIN, WHITE, ball)

        # Update the display
        pygame.display.update()

    # Quit the game
    pygame.quit()


def multiplayer():
    global player2_remaining_time_display, player1_remaining_time_display, pause, music_enabled, sound_effect_enabled, player1_remaining_time, player2_remaining_time, player1_power_up, player2_power_up, player1_active, player2_active, player1_rumble, player2_rumble, player1_score, player2_score, player1_power_up_end_time, player2_power_up_end_time

    pygame.mixer.stop()
    sound("game_track")
    reset_game()
    player1_score = 0
    player2_score = 0

    # Game loop
    running = True
    while running:
        # Handle events
        if pause:
            draw_pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_r:
                    reset_game()
                elif event.key == K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == K_z:
                    player1_score += 1

                elif event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                        sound("unpause")
                    else:
                        pause = True
                        sound("pause")

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

        if not pause:
            score(True)

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

            if (
                player1_power_up
                and pygame.time.get_ticks() >= player1_power_up_end_time
            ):
                player1_active = False

                player1_remaining_time = (
                    countdown_seconds * 1000
                )  # Reset the remaining time for player 1

            if (
                player2_power_up
                and pygame.time.get_ticks() >= player2_power_up_end_time
            ):
                player2_active = False

                player2_remaining_time = (
                    countdown_seconds * 1000
                )  # Reset the remaining time for player 1

            # Makes paddle big and hit ball harder
            if player1_active:
                if player1_rumble == "Inverse":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    paddle_movement(False, 1, PADDLE_SPEED, True)

                if player1_rumble == "Sonic":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    if player2_rumble == "Boomer" and player2_active:
                        paddle_movement(False, 2, PADDLE_SPEED * 2, False)
                    else:
                        paddle_movement(False, 1, PADDLE_SPEED * 2, False)

                if player1_rumble == "Boomer":
                    paddle_movement(True, 2, PADDLE_SPEED, False)

                if player1_rumble == "Slow":
                    paddle_movement(True, 1, PADDLE_SPEED, False)
                    paddle_movement(False, 2, -1, False)

            else:
                paddle_movement(True, 1, PADDLE_SPEED, False)

            if player2_active:
                if player2_rumble == "Inverse":
                    paddle_movement(False, 1, PADDLE_SPEED, False)
                    paddle_movement(True, 1, PADDLE_SPEED, True)

                if player2_rumble == "Sonic":
                    paddle_movement(False, 1, PADDLE_SPEED, False)
                    if player1_rumble == "Boomer" and player1_active:
                        paddle_movement(True, 2, PADDLE_SPEED * 2, False)
                    else:
                        paddle_movement(True, 1, PADDLE_SPEED * 2, False)

                if player2_rumble == "Boomer":
                    paddle_movement(False, 2, PADDLE_SPEED, False)

                if player2_rumble == "Slow":
                    paddle_movement(False, 1, PADDLE_SPEED, False)
                    paddle_movement(True, 2, -1, False)
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

            player1_remaining_time_display = round(
                float(player1_remaining_time / 1000), 2
            )
            player2_remaining_time_display = round(
                float(player2_remaining_time / 1000), 2
            )

        # Draw the remaining time for player 1 on the screen
        player1_timer_text = power_up_font.render(
            str(player1_remaining_time_display), True, WHITE
        )
        player1_ready_text = power_up_font.render(
            f"Ready! {player1_rumble}", True, WHITE
        )
        player2_ready_text = power_up_font.render(
            f"Ready! {player2_rumble}", True, WHITE
        )
        power_up_text = power_up_font.render(f"{player1_rumble}!", True, WHITE)

        if player1_power_up:
            WIN.blit(
                player1_ready_text,
                (WIDTH // 4 - player1_ready_text.get_width() // 2, 20),
            )
        elif player1_active:
            WIN.blit(
                power_up_text, (WIDTH // 4 - player1_timer_text.get_width() // 2, 20)
            )
        else:
            WIN.blit(
                player1_timer_text,
                (WIDTH // 4 - player1_timer_text.get_width() // 2, 20),
            )

        # Draw the remaining time for player 2 on the screen
        player2_timer_text = power_up_font.render(
            str(player2_remaining_time_display), True, WHITE
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
        score_text = score_font.render(
            f"{player1_score} - {player2_score}", True, WHITE
        )
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

        pygame.draw.ellipse(WIN, WHITE, ball)

        # Update the display
        pygame.display.update()

    # Quit the game
    pygame.quit()


def options():
    global sound_effect_enabled, music_enabled, music_option
    while True:
        if music_enabled:
            music_option = "Music ON"
            pygame.mixer.music.unpause()
        else:
            music_option = "Music OFF"
            pygame.mixer.music.pause()

        if sound_effect_enabled:
            sound_effect_option = "Sound Effects ON"

        else:
            sound_effect_option = "Sound Effects OFF"

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill((29, 1, 18, 255))

        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH / 2, HEIGHT * 0.2))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        MUSIC_TOGGLE = Button(
            image=None,
            pos=(WIDTH / 2, HEIGHT * 0.4),
            text_input=music_option,
            font=get_font(75),
            base_color="White",
            hovering_color="#d7fcd4",
        )

        SOUND_EFFECT_TOGGLE = Button(
            image=None,
            pos=(WIDTH / 2, HEIGHT * 0.6),
            text_input=sound_effect_option,
            font=get_font(75),
            base_color="White",
            hovering_color="#d7fcd4",
        )

        OPTIONS_BACK = Button(
            image=pygame.image.load(r"assets\Quit Rect.png"),
            pos=(WIDTH / 2, HEIGHT * 0.8),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="#d7fcd4",
        )

        for button in [MUSIC_TOGGLE, SOUND_EFFECT_TOGGLE, OPTIONS_BACK]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    sound("button")
                    main_menu()
                elif MUSIC_TOGGLE.checkForInput(OPTIONS_MOUSE_POS):
                    sound("button")
                    music_enabled = not music_enabled
                elif SOUND_EFFECT_TOGGLE.checkForInput(OPTIONS_MOUSE_POS):
                    sound("button")
                    sound_effect_enabled = not sound_effect_enabled

        pygame.display.update()


def main_menu():
    global player1_score, player2_score
    while True:
        SCREEN.fill((29, 1, 18, 255))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, HEIGHT * 0.2))

        MULTIPLAYER_BUTTON = Button(
            image=pygame.image.load(r"assets\Options Rect.png"),
            pos=(WIDTH / 2, HEIGHT * 0.4),
            text_input="2 Player",
            font=get_font(70),
            base_color="White",
            hovering_color="#d7fcd4",
        )

        SINGLEPLAYER_BUTTON = Button(
            image=pygame.image.load(r"assets\Options Rect.png"),
            pos=(WIDTH / 2, HEIGHT * 0.5),
            text_input="1 Player",
            font=get_font(70),
            base_color="White",
            hovering_color="#d7fcd4",
        )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load(r"assets\Options Rect.png"),
            pos=(WIDTH / 2, HEIGHT * 0.7),
            text_input="OPTIONS",
            font=get_font(75),
            base_color="White",
            hovering_color="#d7fcd4",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load(r"assets\Quit Rect.png"),
            pos=(WIDTH / 2, HEIGHT * 0.9),
            text_input="QUIT",
            font=get_font(75),
            base_color="White",
            hovering_color="#d7fcd4",
        )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [
            MULTIPLAYER_BUTTON,
            SINGLEPLAYER_BUTTON,
            OPTIONS_BUTTON,
            QUIT_BUTTON,
        ]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MULTIPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound("button")
                    multiplayer()
                if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound("button")

                    singleplayer()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound("button")
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound("button")
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def sound(type):
    if sound_effect_enabled:
        if type == "button":
            button_effect.play()
        if type == "paddle":
            paddle_effect.play()
        if type == "wall":
            wall_effect.play()
        if type == "point":
            point_effect.play()
        if type == "laser":
            laser_effect.play()

    else:
        return None

    if music_enabled:
        if type == "game_track":
            pygame.mixer.music.load(game_track)
            pygame.mixer.music.play(-1)
        if type == "main_menu":
            pygame.mixer.music.load(main_menu_track)
            pygame.mixer.music.play(-1)
        if type == "jazz_menu":
            pygame.mixer.music.load(jazz_menu_track)
            pygame.mixer.music.play(-1)
    else:
        return None

    if type == "pause":
        pygame.mixer.music.pause()
    elif type == "unpause":
        if music_enabled:
            pygame.mixer.music.unpause()
    else:
        return None


def menu():
    pygame.mixer.stop()
    sound("jazz_menu")
    main_menu()


menu()
