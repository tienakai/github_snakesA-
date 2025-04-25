# Thư viện game
import pygame
import random
import heapq

pygame.init()

# Cài đặt cửa sổ và màu
WIDTH, HEIGHT = 700, 700
CELL_SIZE = 35
GRID_SIZE = WIDTH // CELL_SIZE
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake A* Game")
icon = pygame.image.load(r"D:\pythonA_game\FileGame\assets\yellowbird-downflap.png")
pygame.display.set_icon(icon)

BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)
RED = (255, 0, 0)

# Font và điểm số
score = 0
font = pygame.font.SysFont(None, 36)
def draw_score(display, score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    display.blit(text, (10, 10))
    

# Rắn
snake = [(2, 2)]

# Tạo mồi ngẫu nhiên
def generate_food(snake_body):
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake_body:
            return pos

food = generate_food(snake)

# A* thuật toán tìm đường
def astar(start, goal, snake_body):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and
                    neighbor not in snake_body):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current
    return []

# Vòng lặp game
running = True
while running:
    clock.tick(5)
    display.fill(BG_COLOR)

    # Vẽ lưới
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(display, BLACK, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i))
        pygame.draw.line(display, BLACK, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))

    # Tìm đường đi tới mồi
    path = astar(snake[0], food, snake)

    if path:
        new_head = path[0]
        snake.insert(0, new_head)
        if new_head == food:
            food = generate_food(snake)
            score += 1
        else:
            snake.pop()
    else:
        print("Không tìm được đường đi!")
        running = False

    # Vẽ rắn
    for part in snake:
        pygame.draw.rect(display, PINK, (part[0] * CELL_SIZE, part[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Vẽ mồi
    pygame.draw.rect(display, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_score(display, score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()