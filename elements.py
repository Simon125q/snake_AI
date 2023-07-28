import random
import pygame
from pygame.math import Vector2
from settings import *

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.head = self.body[0]
        self.direction = [1, 0]

    def draw_snake(self, screen):
        for part in self.body:
            x = part.x * CELL_SIZE
            y = part.y * CELL_SIZE
            part_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, part_rect)

    def move_snake(self, screen, apple, points, can_move):
        if can_move:
            if self.eating(apple):
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(self.direction[0], self.direction[1]))
                self.body = body_copy[:]
                points += 1
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(self.direction[0], self.direction[1]))
                self.body = body_copy[:]
        self.draw_snake(screen)
        return points

    def eating(self, apple):
        if apple.pos == self.body[0]:
            apple.randomize()
            while apple.pos in self.body:
                apple.randomize()
            return True
        else:
            return False

    def check_collision(self, pt = None):
        if pt == None:
            pt = self.body[0]
        for part in self.body[1:]:
            if pt == part:
                print('here')
                return True
        if pt.x < 0 or pt.y < 0 or pt.x > COLUMNS - 1 or pt.y > ROWS - 1:
            print("no, here")
            return True
        return False
                  
class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self, screen, points):
        apple_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if points % 5 == 0 and points != 0:
            screen.blit(APPLE_GOLD, apple_rect)
        else:
            screen.blit(APPLE_RED, apple_rect)

    def randomize(self):
        self.x = random.randint(0, COLUMNS - 1)
        self.y = random.randint(0, ROWS - 1)
        self.pos = Vector2(self.x, self.y)
