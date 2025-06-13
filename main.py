import pygame
import random
import heapq
from pygame.math import Vector2

pygame.init()
pygame.mixer.init()
eat_sound = pygame.mixer.Sound(r"D:\pythonA_game\FileGame\sound\sfx_point.wav")
# Cài đặt cửa sổ và màu
WIDTH, HEIGHT = 700, 700
CELL_SIZE = 35
GRID_SIZE = WIDTH // CELL_SIZE
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake A* Game")

BG_COLOR = (175, 215, 70)
WHITE = (255, 255, 255)

#TỐC ĐỘ BAN ĐẦU 
speed = 8

# Load ảnh tạm dừng và tiếp tục
is_paused = False
pause_img = pygame.image.load(r"D:\pythonA_game\FileGame\assets\pause.png")
pause_img = pygame.transform.scale(pause_img, (40, 40))
play_img = pygame.image.load(r"D:\pythonA_game\FileGame\assets\play.png")
play_img = pygame.transform.scale(play_img, (40, 40))
pause_rect = pause_img.get_rect(topright=(WIDTH - 10, 10))

# Load ảnh
food_img = pygame.image.load(r"C:\Users\Administrator\Downloads\snake_graphics\Graphics\apple.png")
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

# Font điểm số
score = 0
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 60)
menu_font = pygame.font.SysFont(None, 40)

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

def generate_food(snake_body):
    while True:
        pos = Vector2(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if tuple(pos) not in set(tuple(b) for b in snake_body):
            return pos

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

def get_safe_move(head, body_set):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)  # Trộn ngẫu nhiên hướng đi
    for d in directions:
        next_pos = (head[0] + d[0], head[1] + d[1])
        if (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE and next_pos not in body_set):
            return next_pos
    return None


# === Chế độ chọn ===
mode = None

def show_start_screen():
    display.fill(BG_COLOR)

    # Render title
    title = title_font.render("SNAKE A* GAME", True, (0, 100, 0))
    title_pos = (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100)
    display.blit(title, title_pos)

    # Load ảnh nền nút
    button_img = pygame.image.load(r"D:\pythonA_game\kenney_ui-pack\PNG\Blue\Default\button_rectangle_depth_gradient.png")
    button_img = pygame.transform.scale(button_img, (350, 50))  # kích thước nút

    # Tạo text
    player_text = menu_font.render("Press 1 to play manually", True, (255, 255, 255))
    bot_text = menu_font.render("Press 2 to let the bot play", True, (255, 255, 255))

    # Vị trí các nút
    player_button_pos = (WIDTH // 2 - 150, HEIGHT // 2)
    bot_button_pos = (WIDTH // 2 - 150, HEIGHT // 2 + 70)

    # Hiển thị ảnh nút
    display.blit(button_img, player_button_pos)
    display.blit(button_img, bot_button_pos)

    # Hiển thị text căn giữa trên nút
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

    # Tiêu đề END
    end_text = title_font.render("END", True, (200, 0, 0))
    display.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 100))

    # Load ảnh nền nút
    end_button_img = pygame.image.load(r"D:\pythonA_game\kenney_ui-pack\PNG\Yellow\Default\button_rectangle_depth_gloss.png")
    end_button_img = pygame.transform.scale(end_button_img, (450, 60))  # chỉnh chiều cao nhẹ

    # Tạo chữ trên nút
    prompt = menu_font.render("Press Q to Quit or R to Reset", True, (0, 0, 0))

    # Tính vị trí nút để căn giữa
    button_pos = (WIDTH // 2 - end_button_img.get_width() // 2, HEIGHT // 2 + 20)
    display.blit(end_button_img, button_pos)

    # Vẽ chữ căn giữa trong ảnh nút
    text_pos = (
        button_pos[0] + (end_button_img.get_width() - prompt.get_width()) // 2,
        button_pos[1] + (end_button_img.get_height() - prompt.get_height()) // 2
    )
    display.blit(prompt, text_pos)

    pygame.display.flip()



#----------------------------------------------------------------------------------------------
#Phần chơi chính 

while True:
    mode = None
    speed = 8
    snake = SNAKE()
    food = generate_food(snake.body)
    score = 0

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

    # For bot mode, keep track of direction
    if mode == 'bot':
        # Initialize direction from initial snake body
        direction = snake.body[0] - snake.body[1]
        if direction.length_squared() == 0:
            direction = Vector2(1, 0)

    while running:
        clock.tick(speed)
        # Nếu đang pause, vẻ game và chờ nhấn play
        if is_paused:
            display.fill(BG_COLOR)
            for i in range(GRID_SIZE + 1):
                pygame.draw.line(display, WHITE, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i))
                pygame.draw.line(display, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))

            draw_score(display, score)
            display.blit(food_img, (int(food.x * CELL_SIZE), int(food.y * CELL_SIZE)))
            snake.draw_snake()
            display.blit(play_img, pause_rect)  # Vẽ nút play
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        is_paused = False
            continue

        display.fill(BG_COLOR)
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(display, WHITE, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i))
            pygame.draw.line(display, WHITE, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT))

    # Xử lý điều khiển cho player mode
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

        elif mode == 'bot':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        is_paused = True

    # Logic cập nhật game và di chuyển snake
        head = tuple(snake.body[0])
        body_set = set(tuple(part) for part in snake.body)
        new_head = None

        if mode == 'bot':
            path_to_food = astar(head, tuple(food), body_set)
            if path_to_food:
                new_head = path_to_food[0]
                direction = Vector2(new_head) - snake.body[0]
            else:
                safe_move = get_safe_move(head, body_set)
                if safe_move:
                    new_head = Vector2(safe_move)
                    direction = Vector2(new_head) - snake.body[0]
                else:
                    new_head = snake.body[0] + direction
        else:
            direction = pending_direction
            new_head = snake.body[0] + direction
            if not (0 <= new_head.x < GRID_SIZE and 0 <= new_head.y < GRID_SIZE) or tuple(new_head) in body_set:
                game_over = True
                running = False

        if new_head:
            if not (0 <= new_head.x < GRID_SIZE and 0 <= new_head.y < GRID_SIZE) or tuple(new_head) in body_set:
                game_over = True
                running = False
            else:
                if Vector2(new_head) == food:
                    snake.new_block = True
                    food = generate_food(snake.body)
                    score += 1
                    eat_sound.play()
                    speed += 0.5
                snake.move(Vector2(new_head))
                if len(snake.body) != len(set(tuple(b) for b in snake.body)):
                    game_over = True
                    running = False

        snake.draw_snake()
        display.blit(food_img, (int(food.x * CELL_SIZE), int(food.y * CELL_SIZE)))
        draw_score(display, score)
        display.blit(pause_img if not is_paused else play_img, pause_rect)
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
                    # Reset state to show start screen again
                    running = False
                    game_over = False
                    mode = None



