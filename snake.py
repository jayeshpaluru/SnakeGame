import pygame
import sys
import random
from pygame.locals import *

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
CELL_SIZE = WIDTH // GRID_WIDTH

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game speed
FPS = 60
SNAKE_SPEED = 10

# Lerp speed
LERP_SPEED = 0.1

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.lerp_body = [((GRID_WIDTH // 2) * CELL_SIZE, (GRID_HEIGHT // 2) * CELL_SIZE)]
        self.direction = RIGHT

    def change_direction(self, new_direction):
        if new_direction[0] == -self.direction[0] or new_direction[1] == -self.direction[1]:
            return
        self.direction = new_direction

    def move(self):
        x, y = self.body[0]
        x = (x + self.direction[0]) % GRID_WIDTH
        y = (y + self.direction[1]) % GRID_HEIGHT

        if (x, y) in self.body[1:]:
            return False

        self.body.insert(0, (x, y))
        self.body.pop()
        return True

    
    def grow(self):
        self.body.append(self.body[-1])
        self.lerp_body.append(self.lerp_body[-1])
        
    def lerp_move(self):
        new_lerp_body = []
        for i in range(len(self.body)):
            x1, y1 = self.lerp_body[i]
            x2, y2 = self.body[i]
            x2, y2 = x2 * CELL_SIZE, y2 * CELL_SIZE
            new_x = x1 + (x2 - x1) * LERP_SPEED
            new_y = y1 + (y2 - y1) * LERP_SPEED
            new_lerp_body.append((new_x, new_y))
        self.lerp_body = new_lerp_body

def spawn_food(snake_body):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake_body:
            return (x, y)

def draw(screen, snake, food, score, high_score):
    screen.fill(WHITE)

    for x, y in snake.lerp_body:
        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_text(screen, f"Score: {score}", 36, WIDTH // 2, 10, (0, 0, 0))
    draw_text(screen, f"High Score: {high_score}", 36, WIDTH // 2, HEIGHT - 40, (0, 0, 0))

    pygame.display.flip()


def draw_text(screen, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    high_score = load_high_score()

    while True:
        snake = Snake()
        food = spawn_food(snake.body)
        score = 0

        frame_count = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        snake.change_direction(UP)
                    elif event.key == K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == K_RIGHT:
                        snake.change_direction(RIGHT)

            if frame_count % (FPS // SNAKE_SPEED) == 0:
                if not snake.move():
                    break  # Game over

                if snake.body[0] == food:
                    snake.grow()
                    food = spawn_food(snake.body)
                    score += 10

            snake.lerp_move()
            draw(screen, snake, food, score, high_score)
            clock.tick(FPS)
            frame_count += 1
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        draw_text(screen, "Game Over", 48, WIDTH // 2, HEIGHT // 2 - 50, RED)
        draw_text(screen, "Press any key to restart", 24, WIDTH // 2, HEIGHT // 2, (0, 0, 0))
        pygame.display.flip()

        # Wait for a key press to restart the game
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                break

if __name__ == "__main__":
    main()
