# === Imports ===
import cv2  # Cam input
import mediapipe as mp  # Hand tracking
import pygame  # Game lib
import numpy as np  # Math ops
import random  # Random vals

# === Mediapipe Init ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# === Pygame Init ===
pygame.init()
screen_width, screen_height = 800, 300  # Narrow field
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Title
clock = pygame.time.Clock()

# === Colors ===
WHITE = (255, 255, 255)  # Lines & scores
BLACK = (0, 0, 0)  # BG
YELLOW = (255, 255, 0)  # Ball
RED = (255, 0, 0)  # No hand
GREEN = (0, 255, 0)  # Hand ok

# === Sizes ===
paddle_width = 5
paddle_height = 40  # Small paddles
ball_radius = 8  # Small ball

# === Ball Vars ===
initial_speed = 7  # Start speed
speed_increment = 0.5  # Accel per bounce

# === Game Vars ===
ball_x, ball_y = screen_width // 2, screen_height // 2
ball_speed_x = initial_speed * random.choice((1, -1))
ball_speed_y = initial_speed * random.choice((1, -1))
left_paddle_x = 30
right_paddle_x = screen_width - 40
left_score, right_score = 0, 0  # Scores
game_started = False  # Start flag

# === Paddle Vars ===
left_paddle_y = screen_height // 2 - paddle_height // 2
right_paddle_y = screen_height // 2 - paddle_height // 2
max_paddle_speed = 10  # Limit paddle speed

# === Fonts ===
font = pygame.font.SysFont('Arial', 24)
score_font = pygame.font.SysFont('Arial', 48)

# === Webcam Init ===
cap = cv2.VideoCapture(0)  # Open cam


# === Reset ball pos ===
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, game_started
    ball_x, ball_y = screen_width // 2, screen_height // 2
    ball_speed_x = initial_speed * random.choice((1, -1))
    ball_speed_y = initial_speed * random.choice((1, -1))
    game_started = False


# === Main loop ===
try:
    running = True
    while running:
        # === Cam feed ===
        ret, frame = cap.read()
        if not ret:
            print("Cam error.")  # Error msg
            break

        # === Process cam ===
        frame = cv2.flip(frame, 1)  # Mirror
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)  # Track hands

        # === Draw BG ===
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height), 2)  # Mid line

        # === Paddle colors ===
        left_color, right_color = RED, RED  # Default red

        # === Hand detection ===
        left_detected = False
        right_detected = False

        # === Process hands ===
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Index tip
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Left paddle
                if handedness.classification[0].label == 'Left':
                    left_detected = True
                    target_y = int(index_tip.y * screen_height) - paddle_height // 2
                    left_color = GREEN  # Green when detected
                    dy = target_y - left_paddle_y
                    left_paddle_y += max(-max_paddle_speed, min(max_paddle_speed, dy))  # Smooth move

                # Right paddle
                elif handedness.classification[0].label == 'Right':
                    right_detected = True
                    target_y = int(index_tip.y * screen_height) - paddle_height // 2
                    right_color = GREEN  # Green when detected
                    dy = target_y - right_paddle_y
                    right_paddle_y += max(-max_paddle_speed, min(max_paddle_speed, dy))  # Smooth move

        # === Limit paddle move ===
        left_paddle_y = max(0, min(screen_height - paddle_height, left_paddle_y))
        right_paddle_y = max(0, min(screen_height - paddle_height, right_paddle_y))

        # === Game start ===
        if left_detected and right_detected and not game_started:
            left_index = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            right_index = results.multi_hand_landmarks[1].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            distance = np.hypot((right_index.x - left_index.x) * screen_width,
                                (right_index.y - left_index.y) * screen_height)
            if distance < 50:  # Start on close index
                game_started = True

        # === Ball movement ===
        if game_started:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Bounce ball
            if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
                ball_speed_y *= -1

            # Paddle bounce
            if pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height).colliderect(
                    (ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)) or \
                    pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height).colliderect(
                        (ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                ball_speed_x *= -1
                ball_speed_x += speed_increment * np.sign(ball_speed_x)
                ball_speed_y += speed_increment * np.sign(ball_speed_y)

            # Update score
            if ball_x < 0:
                right_score += 1
                reset_ball()
            elif ball_x > screen_width:
                left_score += 1
                reset_ball()

        # === Draw paddles and ball ===
        pygame.draw.rect(screen, left_color, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, right_color, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, YELLOW, (ball_x, ball_y), ball_radius)

        # Draw scores
        screen.blit(score_font.render(str(left_score), True, WHITE), (200, 10))
        screen.blit(score_font.render(str(right_score), True, WHITE), (600, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

finally:
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
