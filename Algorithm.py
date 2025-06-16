import pygame
import random
import heapq
import os
from pygame.math import Vector2
from collections import deque

# Initialize Pygame
pygame.init()
pygame.mixer.init()
def astar(start, goal, snake_body):
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

    return None

def get_safe_move(head, body):
    body_set = set(tuple(part) for part in body)
    tail = tuple(body[-1])
    body_set_without_tail = body_set - {tail}

    path_to_tail = astar(head, tail, body_set_without_tail)
    if path_to_tail:
        return path_to_tail[0]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    max_area = -1
    best_move = None

    for d in directions:
        next_pos = (head[0] + d[0], head[1] + d[1])
        if not (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE) or next_pos in body_set:
            continue

        visited = set()
        queue = deque([next_pos])
        visited.add(next_pos)
        max_depth = 100  # Limit depth to improve performance
        depth = 0

        while queue and depth < max_depth:
            current = queue.popleft()
            for nd in directions:
                neighbor = (current[0] + nd[0], current[1] + nd[1])
                if (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE
                        and neighbor not in body_set and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append(neighbor)
            depth += 1

        if len(visited) > max_area:
            max_area = len(visited)
            best_move = next_pos

    return best_move

def get_away_from_food(head, food, body):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    max_distance = -1
    best_move = None
    body_set = set(tuple(b) for b in body)

    for d in directions:
        next_pos = (head[0] + d[0], head[1] + d[1])
        if not (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE) or next_pos in body_set:
            continue
        distance = abs(next_pos[0] - food[0]) + abs(next_pos[1] - food[1])
        if distance > max_distance:
            max_distance = distance
            best_move = next_pos

    return best_move