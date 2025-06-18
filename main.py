import pygame
import random
import heapq
import os
from pygame.math import Vector2
from collections import deque, defaultdict

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 700, 700
CELL_SIZE = 35
GRID_SIZE = WIDTH // CELL_SIZE 
BG_COLOR = (175, 215, 70)
WHITE = (255, 255, 255)
INITIAL_SPEED = 5
MAX_SPEED = 20
DIRECTIONS = [Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0)]  # Precomputed directions
MAX_BFS_DEPTH = 300  # Increased BFS depth for better exploration

# Set up display and clock
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load sound with error handling
try:
    eat_sound = pygame.mixer.Sound(r"D:\pythonA_game\FileGame\sound\sfx_point.wav")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    pygame.quit()
    exit()

# Load pause/play images
try:
    pause_img = pygame.image.load(r"D:\pythonA_game\FileGame\assets\pause.png")
    pause_img = pygame.transform.scale(pause_img, (40, 40))
    play_img = pygame.image.load(r"D:\pythonA_game\FileGame\assets\play.png")
    play_img = pygame.transform.scale(play_img, (40, 40))
except pygame.error as e:
    print(f"Error loading pause/play images: {e}")
    pygame.quit()
    exit()

pause_rect = pause_img.get_rect(topright=(WIDTH - 10, 10))

# Load food image
try:
    food_img = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\apple.png")
    food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))
except pygame.error as e:
    print(f"Error loading food image: {e}")
    pygame.quit()
    exit()

# Load button images
try:
    button_img = pygame.image.load(r"D:\pythonA_game\kenney_ui-pack\PNG\Blue\Default\button_rectangle_depth_gradient.png")
    button_img = pygame.transform.scale(button_img, (350, 50))
    end_button_img = pygame.image.load(r"D:\pythonA_game\kenney_ui-pack\PNG\Yellow\Default\button_rectangle_depth_gloss.png")
    end_button_img = pygame.transform.scale(end_button_img, (450, 60))
except pygame.error as e:
    print(f"Error loading button images: {e}")
    pygame.quit()
    exit()

# Fonts
score_font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 60)
menu_font = pygame.font.SysFont(None, 40)

# Game state
is_paused = False
score = 0
speed = INITIAL_SPEED
mode = None

# Path caching
path_cache = defaultdict(lambda: None)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]  # Changed starting position
        self.new_block = False
        self.load_images()
        self.head = self.head_right
        self.tail = self.tail_right

    def load_images(self):
        try:
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
        except pygame.error as e:
            print(f"Error loading snake images: {e}")
            pygame.quit()
            exit()

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

def generate_food(snake_body):
    body_set = set(tuple(b) for b in snake_body)
    while True:
        pos = Vector2(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if tuple(pos) not in body_set:
            return pos

def astar(start, goal, snake_body):
    cache_key = (tuple(start), tuple(goal), tuple(tuple(b) for b in snake_body))
    if path_cache[cache_key]:
        return path_cache[cache_key]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start = tuple(start)
    goal = tuple(goal)
    snake_body = set(tuple(b) for b in snake_body)
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
            path_cache[cache_key] = path
            return path

        for d in DIRECTIONS:
            neighbor = (current[0] + d.x, current[1] + d.y)
            if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in snake_body):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current

    path_cache[cache_key] = None
    return None

def bfs_survival(head, body):
    body_set = set(tuple(part) for part in body)
    tail = tuple(body[-1])
    body_set_without_tail = body_set - {tail}
    max_safety_score = -float('inf')
    best_move = None
    valid_moves = []

    # Check all possible moves
    for d in DIRECTIONS:
        next_pos = (head[0] + d.x, head[1] + d.y)
        if (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE and next_pos not in body_set):
            valid_moves.append(next_pos)

    # Special handling for top-left corner
    if len(valid_moves) > 0 and head[0] == 0 and head[1] == 0:
        print(f"Top-left corner detected at {head}, valid moves: {valid_moves}")
        for move in valid_moves:
            # Check safety for next three moves
            next_next_pos = (move[0] + (move[0] - head[0]), move[1] + (move[1] - head[1]))
            safe = False
            if (0 <= next_next_pos[0] < GRID_SIZE and 0 <= next_next_pos[1] < GRID_SIZE and
                next_next_pos not in body_set):
                for d2 in DIRECTIONS:
                    next_next_next_pos = (next_next_pos[0] + d2.x, next_next_pos[1] + d2.y)
                    if (0 <= next_next_next_pos[0] < GRID_SIZE and 0 <= next_next_next_pos[1] < GRID_SIZE and
                        next_next_next_pos not in body_set):
                        safe = True
                        break
            else:
                safe = False

            # Safety score: force right if possible, high penalty for unsafe
            safety_score = 200 if move[0] > head[0] else 100  # Strong preference for right
            safety_score += 100 if safe else -100  # High bonus for safety, penalty for unsafe
            if safety_score > max_safety_score:
                max_safety_score = safety_score
                best_move = move
        if not best_move and valid_moves:
            # Force move right if available, otherwise first valid
            for move in valid_moves:
                if move[0] > head[0]:
                    best_move = move
                    break
            if not best_move:
                best_move = valid_moves[0]
        print(f"Top-left move chosen: {best_move}, safety score: {max_safety_score}")
        return best_move

    # General corner/edge handling
    if len(valid_moves) > 0 and (
        (head[0] == 0 or head[0] == GRID_SIZE-1) or
        (head[1] == 0 or head[1] == GRID_SIZE-1)
    ):
        print(f"Corner/edge detected at {head}, valid moves: {valid_moves}")
        for move in valid_moves:
            if (head[0] == 0 and move[0] > head[0]) or (head[0] == GRID_SIZE-1 and move[0] < head[0]) or \
               (head[1] == 0 and move[1] > head[1]) or (head[1] == GRID_SIZE-1 and move[1] < head[1]):
                best_move = move
                break
        if not best_move:
            best_move = valid_moves[0]
        print(f"Corner move chosen: {best_move}")
        return best_move

    # BFS with multi-step safety
    center = (GRID_SIZE // 2, GRID_SIZE // 2)
    for next_pos in valid_moves:
        visited = set([next_pos])
        queue = deque([next_pos])
        depth = 0
        safe = True
        while queue and depth < MAX_BFS_DEPTH:
            current = queue.popleft()
            next_neighbors = 0
            for nd in DIRECTIONS:
                neighbor = (current[0] + nd.x, current[1] + nd.y)
                if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE
                        and neighbor not in body_set_without_tail and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append(neighbor)
                    next_neighbors += 1
            if next_neighbors == 0:
                safe = False
                break
            depth += 1

        if not safe:
            continue

        path_to_tail = astar(next_pos, tail, body_set_without_tail)
        safety_score = len(visited) * (1.5 if path_to_tail else 1.0) + abs(next_pos[0] - center[0]) + abs(next_pos[1] - center[1])
        if safety_score > max_safety_score:
            max_safety_score = safety_score
            best_move = next_pos

    if not best_move and valid_moves:
        best_move = random.choice(valid_moves)
        print(f"Random safe move chosen: {best_move}, safety score: {max_safety_score}")

    if best_move:
        print(f"Survival move chosen: {best_move}, safety score: {max_safety_score}")
    else:
        print(f"No survival move found, valid moves: {valid_moves}")
    return best_move

def tail_chasing_fallback(head, body):
    tail = tuple(body[-1])
    body_set_without_tail = set(tuple(part) for part in body) - {tail}
    path_to_tail = astar(head, tail, body_set_without_tail)
    if path_to_tail:
        print(f"Tail-chasing move: {path_to_tail[0]}")
        return path_to_tail[0]

    # Fallback: choose any valid move
    body_set = set(tuple(part) for part in body)
    valid_moves = [
        (head[0] + d.x, head[1] + d.y)
        for d in DIRECTIONS
        if (0 <= head[0] + d.x < GRID_SIZE and
            0 <= head[1] + d.y < GRID_SIZE and
            (head[0] + d.x, head[1] + d.y) not in body_set)
    ]
    if valid_moves:
        move = random.choice(valid_moves)
        print(f"Fallback move: {move}")
        return move
    print("No fallback move found")
    return None

def draw_score():
    text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    display.blit(text, (10, 10))

def draw_pause_button():
    display.blit(play_img if is_paused else pause_img, pause_rect)

def draw_game(snake, food, path_to_food=None):
    display.fill(BG_COLOR)
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(display, WHITE, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i))
        pygame.draw.line(display, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))
    if path_to_food and mode == 'bot':
        for step in path_to_food:
            pygame.draw.rect(display, (255, 255, 0), (step[0] * CELL_SIZE, step[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    display.blit(food_img, (int(food.x * CELL_SIZE), int(food.y * CELL_SIZE)))
    snake.draw_snake()
#   draw_score()
    draw_pause_button()

def show_start_screen():
    display.fill(BG_COLOR)
    title = title_font.render("SNAKE A* GAME", True, (0, 100, 0))
    display.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    player_text = menu_font.render("Press 1 to play manually", True, (255, 255, 255))
    bot_text = menu_font.render("Press 2 to let the bot play", True, (255, 255, 255))
    player_button_pos = (WIDTH // 2 - 150, HEIGHT // 2)
    bot_button_pos = (WIDTH // 2 - 150, HEIGHT // 2 + 70)
    display.blit(button_img, player_button_pos)
    display.blit(button_img, bot_button_pos)
    display.blit(player_text, (
        player_button_pos[0] + (button_img.get_width() - player_text.get_width()) // 2,
        player_button_pos[1] + (button_img.get_height() - player_text.get_height()) // 2
    ))
    display.blit(bot_text, (
        bot_button_pos[0] + (button_img.get_width() - bot_text.get_width()) // 2,
        bot_button_pos[1] + (button_img.get_height() - bot_text.get_height()) // 2
    ))
    pygame.display.flip()

def show_end_screen():
    display.fill(BG_COLOR)
    end_text = title_font.render("END", True, (200, 0, 0))
    display.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 100))
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    display.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    prompt = menu_font.render("Press Q to Quit or R to Reset", True, (0, 0, 0))
    button_pos = (WIDTH // 2 - end_button_img.get_width() // 2, HEIGHT // 2 + 20)
    display.blit(end_button_img, button_pos)
    display.blit(prompt, (
        button_pos[0] + (end_button_img.get_width() - prompt.get_width()) // 2,
        button_pos[1] + (end_button_img.get_height() - prompt.get_height()) // 2
    ))
    pygame.display.flip()

# Main game loop
while True:
    mode = None
    speed = INITIAL_SPEED
    snake = SNAKE()
    food = generate_food(snake.body)
    score = 0
    path_cache.clear()
    pygame.display.set_caption(f"Snake A* Game - Score: {score}")  # Initialize title with score

    while mode is None:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 'player'
                elif event.key == pygame.K_2:
                    mode = 'bot'

    direction = Vector2(1, 0)
    pending_direction = direction
    running = True
    game_over = False

    if mode == 'bot':
        direction = snake.body[0] - snake.body[1]
        if direction.length_squared() == 0:
            direction = Vector2(1, 0)

    while running:
        clock.tick(speed)
        if is_paused:
            draw_game(snake, food)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        is_paused = False
            continue

        if mode == 'player':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != Vector2(0, 1):
                        pending_direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN and direction != Vector2(0, -1):
                        pending_direction = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT and direction != Vector2(1, 0):
                        pending_direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != Vector2(-1, 0):
                        pending_direction = Vector2(1, 0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if pause_rect.collidepoint(event.pos):
                         is_paused = True
        else:  # Bot mode
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        is_paused = True

        head = tuple(snake.body[0])
        body_set = set(tuple(part) for part in snake.body)
        new_head = None
        path_to_food = None

        if mode == 'bot':
            path_to_food = astar(head, tuple(food), snake.body)
            if path_to_food:
                new_head = path_to_food[0]
                direction = Vector2(new_head) - snake.body[0]
            else:
                safe_move = bfs_survival(head, snake.body)
                if safe_move:
                    new_head = Vector2(safe_move)
                    direction = Vector2(new_head) - snake.body[0]
                else:
                    tail_move = tail_chasing_fallback(head, snake.body)
                    if tail_move:
                        new_head = Vector2(tail_move)
                        direction = Vector2(new_head) - snake.body[0]
                    else:
                        game_over = True
                        running = False

        else:
            direction = pending_direction
            new_head = snake.body[0] + direction

        if new_head:
            if (new_head.x < 0 or new_head.x >= GRID_SIZE or new_head.y < 0 or new_head.y >= GRID_SIZE or
                new_head in snake.body[1:]):
                game_over = True
                running = False
            else:
                if Vector2(new_head) == food:
                    snake.new_block = True
                    food = generate_food(snake.body)
                    score += 1
                    eat_sound.play()
                    speed = min(speed + 0.5, MAX_SPEED)
                    path_cache.clear()
                    pygame.display.set_caption(f"Snake A* Game - Score: {score}")  # Update title with new score
                snake.move(Vector2(new_head))
                if len(snake.body) != len(set(tuple(b) for b in snake.body)):
                    game_over = True
                    running = False

        draw_game(snake, food, path_to_food)
        pygame.display.flip()

    while game_over:
        show_end_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    running = False
                    game_over = False
                    mode = None