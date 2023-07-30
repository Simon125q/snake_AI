import torch
import random
import numpy as np
from collections import deque
from game import GameAI
from model import QTrainer, Linear_QNet
from helper import plot
from settings import *
from debug import debug

class Agent:
    def __init__(self):
        self.num_of_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, learning_rate = LEARNING_RATE, gamma = self.gamma)
    
    def get_state(self, game):
        head = game.snake.body[0]
        point_left = Point(head.x - CELL_SIZE, head.y)
        point_right = Point(head.x + CELL_SIZE, head.y)
        point_up = Point(head.x, head.y - CELL_SIZE)
        point_down = Point(head.x, head.y + CELL_SIZE)
        
        dir_left = game.snake.direction == LEFT
        dir_right = game.snake.direction == RIGHT
        dir_up = game.snake.direction == UP
        dir_down = game.snake.direction == DOWN
        
        state = [
            # Danger straight
            (dir_right and game.snake.check_collision(point_right)) or 
            (dir_left and game.snake.check_collision(point_left)) or 
            (dir_up and game.snake.check_collision(point_up)) or 
            (dir_down and game.snake.check_collision(point_down)),

            # Danger right
            (dir_up and game.snake.check_collision(point_right)) or 
            (dir_down and game.snake.check_collision(point_left)) or 
            (dir_left and game.snake.check_collision(point_up)) or 
            (dir_right and game.snake.check_collision(point_down)),

            # Danger left
            (dir_down and game.snake.check_collision(point_right)) or 
            (dir_up and game.snake.check_collision(point_left)) or 
            (dir_right and game.snake.check_collision(point_up)) or 
            (dir_left and game.snake.check_collision(point_down)),
            
            # Move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,
            
            # Food location 
            game.apple.x < game.snake.body[0].x,  # food left
            game.apple.x > game.snake.body[0].x,  # food right
            game.apple.y < game.snake.body[0].y,  # food up
            game.apple.y > game.snake.body[0].y  # food down
            ]

        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        self.epsilon = 80 - self.num_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameAI()
    
    while True:
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)
        debug(final_move, y = 40)
        reward, game_over, score = game.run(final_move)
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)
        
        agent.remember(state_old, final_move, reward, state_new, game_over)
        
        if game_over:
            game.reset()
            agent.num_of_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
                
            print('Game: ', agent.num_of_games, 'Score: ', score, 'Record: ', record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.num_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            
    
if __name__ == '__main__':
    train()