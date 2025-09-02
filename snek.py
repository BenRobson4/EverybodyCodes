import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
BLACK = (20, 20, 20)
GREEN = (50, 200, 50)
RED = (220, 50, 50)
WHITE = (240, 240, 240)
GRID_COLOR = (40, 40, 40)
EYE_COLOR = (0, 0, 0)
TONGUE_COLOR = (255, 80, 80)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Snake Simulation")

# Clock
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

# Directions as vectors
DIRECTIONS = {"UP": (0, -CELL_SIZE), "RIGHT": (CELL_SIZE, 0),
              "DOWN": (0, CELL_SIZE), "LEFT": (-CELL_SIZE, 0)}
DIR_ORDER = ["UP", "RIGHT", "DOWN", "LEFT"]  # clockwise order


def turn_direction(current_dir, action):
    idx = DIR_ORDER.index(current_dir)
    if action == "LEFT":
        return DIR_ORDER[(idx - 1) % 4]
    elif action == "RIGHT":
        return DIR_ORDER[(idx + 1) % 4]
    else:
        return current_dir


def move_snake(direction, head):
    dx, dy = DIRECTIONS[direction]
    x, y = head
    x = (x + dx) % WIDTH
    y = (y + dy) % HEIGHT
    return (x, y)


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_snake(snake, direction):
    # Body
    for segment in snake[1:-1]:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    # Tail as triangle
    tail = snake[0]
    next_seg = snake[1]
    tx, ty = tail[0] + CELL_SIZE // 2, tail[1] + CELL_SIZE // 2
    nx, ny = next_seg[0] + CELL_SIZE // 2, next_seg[1] + CELL_SIZE // 2
    perp = CELL_SIZE // 2
    vx, vy = nx - tx, ny - ty
    if vx == 0:
        points = [(tx - perp, ty), (tx + perp, ty), (nx, ny)]
    elif vy == 0:
        points = [(tx, ty - perp), (tx, ty + perp), (nx, ny)]
    else:
        points = [(tx - perp, ty), (tx + perp, ty), (nx, ny)]
    pygame.draw.polygon(screen, GREEN, points)
    # Head
    head = snake[-1]
    pygame.draw.rect(screen, GREEN, pygame.Rect(head[0], head[1], CELL_SIZE, CELL_SIZE))
    # Eyes & tongue
    cx, cy = head[0] + CELL_SIZE // 2, head[1] + CELL_SIZE // 2
    offset, eye_size, tongue_length = CELL_SIZE // 4, 3, CELL_SIZE // 2
    if direction == "UP":
        pygame.draw.circle(screen, EYE_COLOR, (cx - offset, cy - offset), eye_size)
        pygame.draw.circle(screen, EYE_COLOR, (cx + offset, cy - offset), eye_size)
        pygame.draw.line(screen, TONGUE_COLOR, (cx, head[1]), (cx, head[1] - tongue_length), 2)
    elif direction == "DOWN":
        pygame.draw.circle(screen, EYE_COLOR, (cx - offset, cy + offset), eye_size)
        pygame.draw.circle(screen, EYE_COLOR, (cx + offset, cy + offset), eye_size)
        pygame.draw.line(screen, TONGUE_COLOR, (cx, head[1] + CELL_SIZE), (cx, head[1] + CELL_SIZE + tongue_length), 2)
    elif direction == "LEFT":
        pygame.draw.circle(screen, EYE_COLOR, (cx - offset, cy - offset), eye_size)
        pygame.draw.circle(screen, EYE_COLOR, (cx - offset, cy + offset), eye_size)
        pygame.draw.line(screen, TONGUE_COLOR, (head[0], cy), (head[0] - tongue_length, cy), 2)
    elif direction == "RIGHT":
        pygame.draw.circle(screen, EYE_COLOR, (cx + offset, cy - offset), eye_size)
        pygame.draw.circle(screen, EYE_COLOR, (cx + offset, cy + offset), eye_size)
        pygame.draw.line(screen, TONGUE_COLOR, (head[0] + CELL_SIZE, cy), (head[0] + CELL_SIZE + tongue_length, cy), 2)


def run_game(run_number, total_runs, score_counts):
    start_x, start_y = WIDTH // 2, HEIGHT // 2
    snake = [(start_x - CELL_SIZE, start_y),
             (start_x, start_y),
             (start_x + CELL_SIZE, start_y)]
    snake_length, score, direction = 4, 0, "RIGHT"
    apples = [(random.randrange(0, WIDTH, CELL_SIZE),
               random.randrange(0, HEIGHT, CELL_SIZE)) for _ in range(4)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action = random.choices(["STRAIGHT", "LEFT", "RIGHT"], weights=[2, 1, 1])[0]
        direction = turn_direction(direction, action)
        new_head = move_snake(direction, snake[-1])

        if new_head in snake:
            score_counts[score] = score_counts.get(score, 0) + 1
            return score

        snake.append(new_head)

        for i, apple in enumerate(apples):
            if new_head == apple:
                score += 1
                snake_length += 1
                while True:
                    new_apple = (random.randrange(0, WIDTH, CELL_SIZE),
                                 random.randrange(0, HEIGHT, CELL_SIZE))
                    if new_apple not in snake and new_apple not in apples:
                        apples[i] = new_apple
                        break
                break

        if len(snake) > snake_length:
            snake.pop(0)

        # Draw
        screen.fill(BLACK)
        draw_grid()
        for apple in apples:
            pygame.draw.rect(screen, RED, pygame.Rect(apple[0], apple[1], CELL_SIZE, CELL_SIZE))
        draw_snake(snake, direction)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Run: {run_number}/{total_runs}", True, WHITE), (10, 40))

        freq_y = 70
        for s, count in sorted(score_counts.items()):
            screen.blit(font.render(f"{s}: {count}", True, WHITE), (10, freq_y))
            freq_y += 30

        pygame.display.flip()
        clock.tick(15)


def show_summary(scores, score_counts):
    screen.fill(BLACK)
    total = sum(scores)
    avg = total / len(scores)
    best = max(scores)

    lines = [
        f"Simulation complete ({len(scores)} runs)",
        f"Total score: {total}",
        f"Average score: {avg:.2f}",
        f"Best score: {best}",
        "Final score distribution:"
    ]

    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, WHITE), (20, 20 + i * 40))

    # Display full score distribution
    y_offset = 20 + len(lines) * 40
    for score_val, count in sorted(score_counts.items()):
        screen.blit(font.render(f"Score {score_val}: {count}", True, WHITE), (20, y_offset))
        y_offset += 30

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False


# --- Run simulations ---
scores = []
score_counts = {}
total_runs = 50

for i in range(total_runs):
    scores.append(run_game(i + 1, total_runs, score_counts))

show_summary(scores, score_counts)

pygame.quit()
sys.exit()
