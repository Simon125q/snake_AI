import pygame
import sys
import numpy as np
from settings import *
from elements import *

class GameAI:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.pause = False
        self.move_cooldown = 100
        self.reset()
       
    def reset(self):
        self.snake = Snake()
        self.apple = Apple()
        self.points = 0
        self.move_time = 0
        self.can_move = True
        self.game_over = False
        self.frame_iteration = 0
        self.reward = 0
    
    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)
        pygame.display.set_caption("SNAKE")

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.move_time > self.move_cooldown:
            self.can_move = True
        
    def draw(self):
        screen.fill(GREEN)
        self.draw_grass()
        self.apple.draw_apple(screen, self.points)
        curr_points = self.points
        self.points = self.snake.move_snake(screen, self.apple, self.points, self.can_move)
        if curr_points < self.points:
            self.reward = 10
        if self.can_move:
            self.frame_iteration += 1
            self.can_move = False
            self.move_time = pygame.time.get_ticks()
        self.display_points()
        if self.snake.check_collision() or self.frame_iteration > 100 * len(self.snake.body):
            self.reward = -10
            self.game_over = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.snake.direction[0] != -1:
                        self.snake.direction = RIGHT
                elif event.key == pygame.K_LEFT:
                    if self.snake.direction[0] != 1:
                        self.snake.direction = LEFT
                elif event.key == pygame.K_UP:
                    if self.snake.direction[1] != 1:
                        self.snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    if self.snake.direction[1] != -1:
                        self.snake.direction = DOWN
                elif event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
        
    def step(self, action):
        
        clock_wise = [RIGHT, DOWN, LEFT, UP]
        index = clock_wise.index(self.snake.direction)
        
        if np.array_equal(action, STRAIGHT):
            self.snake.direction = clock_wise[index]
        elif np.array_equal(action, RIGHT_TURN):
            next_index = (index + 1) % 4
            self.snake.direction = clock_wise[next_index]
        else:
            next_index = (index - 1) % 4
            self.snake.direction = clock_wise[next_index]
            
                        
    def draw_grass(self):
        y = 0
        while y < ROWS:
            if y % 2 == 0:
                x = 1
            else:
                x = 0
            while x < COLUMNS:
                pygame.draw.rect(screen, DARK_GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                x = x + 2
            y = y + 1
    
    def display_points(self):
        myfont = pygame.font.Font(None, 38)
        msg = myfont.render(f"Points {self.points}", True, (255, 255, 255))
        msg_box = msg.get_rect()
        msg_box.topright = (COLUMNS * CELL_SIZE - 10, 10)
        screen.blit(msg, msg_box)
        
    def run(self):
        while True:
            self.check_events()
            self.cooldown()
            self.update()
            if not self.pause:
                self.draw()
            if self.game_over:
                print(self.reward, self.game_over, self.points)     
                
if __name__ == "__main__":
    game = GameAI()
    game.run()     
