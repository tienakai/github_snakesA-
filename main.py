import pygame
import random
import heapq
from pygame.math import Vector2

pygame.init()

# Cài đặt cửa sổ và màu
WIDTH, HEIGHT = 700, 700
CELL_SIZE = 35
GRID_SIZE = WIDTH // CELL_SIZE
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake A* Game")

BG_COLOR = (175, 215, 70)
WHITE = (255, 255, 255)

# Load ảnh
food_img = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\apple.png")
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

# Font điểm số
score = 0
font = pygame.font.SysFont(None, 36)
def draw_score(display, score):
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    display.blit(text, (10, 10))

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.new_block = False

        # Ảnh các phần rắn
        self.head_up = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\head_up.png").convert_alpha()
        self.head_down = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\head_down.png").convert_alpha()
        self.head_right = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\head_right.png").convert_alpha()
        self.head_left = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\head_left.png").convert_alpha()

        self.tail_up = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_horizontal.png").convert_alpha()
        self.body_tr = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_topright.png").convert_alpha()
        self.body_tl = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_topleft.png").convert_alpha()
        self.body_br = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_bottomright.png").convert_alpha()
        self.body_bl = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\body_bottomleft.png").convert_alpha()

    def update_graphics(self):
        self.update_head_graphics()
        self.update_tail_graphics()

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def draw_snake(self):
        self.update_graphics()
        for index, block in enumerate(self.body):
            x = int(block.x * CELL_SIZE)
            y = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if index == 0:
                display.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                display.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if previous_block.x == next_block.x:
                    display.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    display.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        display.blit(self.body_tr, block_rect)
                    elif (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        display.blit(self.body_tl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        display.blit(self.body_br, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        display.blit(self.body_bl, block_rect)

    def move(self, new_head):
        self.body.insert(0, new_head)
        if not self.new_block:
            self.body.pop()
        else:
            self.new_block = False

# Tạo mồi

def generate_food(snake_body):
    while True:
        pos = Vector2(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake_body:
            return pos

# A* thuật toán

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
                path.insert(0, Vector2(current))
                current = came_from[current]
            return path

        for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in snake_body):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current
    return []
# Tránh va chạm - bước đi an toàn
def get_safe_move(head, body_set):
    for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        next_pos = (head[0] + d[0], head[1] + d[1])
        if (
            0 <= next_pos[0] < GRID_SIZE and
            0 <= next_pos[1] < GRID_SIZE and
            next_pos not in body_set
        ):
            return next_pos
    return None

# Khởi tạo game
snake = SNAKE()
food = generate_food(snake.body)
running = True

# Vòng lặp chính
while running:
    clock.tick(8)
    display.fill(BG_COLOR)

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(display, WHITE, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i))
        pygame.draw.line(display, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))

    head = tuple(snake.body[0])
    body_set = set(tuple(part) for part in snake.body)
    tail = tuple(snake.body[-1])

    # Chiến lược thông minh
    path_to_food = astar(head, tuple(food), body_set)

    if path_to_food:
        future_body = [Vector2(p) for p in path_to_food] + snake.body[:-1]
        future_body_set = set(tuple(part) for part in future_body)
        path_to_tail = astar(tuple(future_body[0]), tail, future_body_set)

        if path_to_tail or food == snake.body[-1]:
            new_head = path_to_food[0]
        else:
            path_to_tail = astar(head, tail, body_set)
            if path_to_tail:
                new_head = path_to_tail[0]
            else:
                new_head = get_safe_move(head, body_set)
    else:
        path_to_tail = astar(head, tail, body_set)
        if path_to_tail:
            new_head = path_to_tail[0]
        else:
            new_head = get_safe_move(head, body_set)

    if new_head:
        if Vector2(new_head) == food:
            snake.new_block = True
            food = generate_food(snake.body)
            score += 1
        snake.move(Vector2(new_head))
    else:
        print("Không tìm được đường an toàn!")
        running = False

    snake.draw_snake()
    display.blit(food_img, (int(food.x * CELL_SIZE), int(food.y * CELL_SIZE)))
    draw_score(display, score)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()