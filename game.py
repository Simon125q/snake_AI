import pygame
import sys
from settings import *
from elements import *

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.pause = False
        
        self.snake = Snake()
        self.apple = Apple()
        self.points = 0
        self.move_time = 0
        self.move_cooldown = 100
        self.can_move = True
        
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
        self.points = self.snake.move_snake(screen, self.apple, self.points, self.can_move)
        if self.can_move:
            self.can_move = False
            self.move_time = pygame.time.get_ticks()
        self.display_points()
        if self.snake.check_collision():
            self.pause = True
            self.points = 0
            self.snake = Snake()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.snake.direction[0] != -1:
                        self.snake.direction = [1, 0]
                elif event.key == pygame.K_LEFT:
                    if self.snake.direction[0] != 1:
                        self.snake.direction = [-1, 0]
                elif event.key == pygame.K_UP:
                    if self.snake.direction[1] != 1:
                        self.snake.direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    if self.snake.direction[1] != -1:
                        self.snake.direction = [0, 1]
                elif event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                        
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
                
if __name__ == "__main__":
    game = Game()
    game.run()     
