import inspect
import os
import random
import sys
from collections import deque

import numpy as np
import torch
import torch.nn.functional as F

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# from snake import SnakeGameAI,Direction,Point
from environments.snake import Direction, Point, SnakeGameAI
from models.enhanced_nn import EnhancedMultiLayerNN, EnhancedMultiLayerTrainer
from scripts.plot import plot
from exceptions.exceptions import (
    EnvCreationException,
    ModelCreationException,
    StateInitException,
    StateManagementException,
    TrainingException,
)

MAX_MEMORY = 100_000
BATCH_SIZE = 1000


class SnakeAgent:
    """
    Brings together the model and the environment and trains the agent,
    using the model
    """

    def __init__(self, learning_rate, hidden_size):
        self.n_games = 0
        self.epsilon = 0.1
        self.learning_rate = learning_rate
        self.hidden_size = hidden_size
        self.gamma = 0.9
        self.name = "SnakeAgent"
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = EnhancedMultiLayerNN(11, self.hidden_size, 3)
        self.trainer = EnhancedMultiLayerTrainer(
            self.model,
            learning_rate=self.learning_rate,
            gamma=self.gamma,
        )

    def get_state(self, game):
        try:
            head = game.snake[0]
            point_l = Point(head.x - 20, head.y)
            point_r = Point(head.x + 20, head.y)
            point_u = Point(head.x, head.y - 20)
            point_d = Point(head.x, head.y + 20)

            dir_l = game.direction == Direction.LEFT
            dir_r = game.direction == Direction.RIGHT
            dir_u = game.direction == Direction.UP
            dir_d = game.direction == Direction.DOWN

            state = [
                (dir_r and game.is_collision(point_r))
                or (dir_l and game.is_collision(point_l))
                or (dir_u and game.is_collision(point_u))
                or (dir_d and game.is_collision(point_d)),
                (dir_u and game.is_collision(point_r))
                or (dir_d and game.is_collision(point_l))
                or (dir_l and game.is_collision(point_u))
                or (dir_r and game.is_collision(point_d)),
                (dir_d and game.is_collision(point_r))
                or (dir_u and game.is_collision(point_l))
                or (dir_r and game.is_collision(point_u))
                or (dir_l and game.is_collision(point_d)),
                dir_l,
                dir_r,
                dir_u,
                dir_d,
                # Food location
                game.food.x < game.head.x,
                game.food.x > game.head.x,
                game.food.y < game.head.y,
                game.food.y > game.head.y,
            ]
            return np.array(state, dtype=int)
        except Exception:
            raise StateInitException

    def remember(self, state, action, reward, next_state, done):
        try:
            self.memory.append((state, action, reward, next_state, done))
        except Exception:
            raise StateManagementException(func="remember")

    def train_long_memory(self):
        try:
            if len(self.memory) > BATCH_SIZE:
                mini_sample = random.sample(self.memory, BATCH_SIZE)
            else:
                mini_sample = self.memory

            states, actions, rewards, next_states, dones = zip(*mini_sample)
            self.trainer.train_step(states, actions, rewards, next_states, dones)
        except Exception:
            raise TrainingException(func="train_long_memory")

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        try:
            final_move = [0, 0, 0]

            if random.uniform(0, 1) < self.epsilon:
                move = random.randint(0, 2)
                final_move[move] = 1
            else:
                state0 = torch.tensor(state, dtype=torch.float)
                prediction = self.model(state0)
                action = torch.argmax(prediction).item()
                final_move[action] = 1

            # Decay epsilon gradually to balance exploration and exploitation
            if self.epsilon > 0.01:
                self.epsilon -= 0.001  # Adjust the decay step as needed

            return final_move
        except Exception as e:
            raise StateManagementException(func="get_action")


def create_model(learning_rate=0.001, hidden_size=32):
    """_summary_

    Args:
        learning_rate (float, optional): Defaults to 0.001.
        hidden_size (int, optional): Defaults to 32.

    Returns:
       SnakeAgent: SnakeAgent Class
    """
    try:
        return SnakeAgent(learning_rate=learning_rate, hidden_size=hidden_size)
    except Exception:
        raise ModelCreationException


def create_env(width=800, height=600, block_size=20, speed=20):
    try:
        return SnakeGameAI(
            width=width, height=height, block_size=block_size, speed=speed
        )
    except Exception:
        raise EnvCreationException


def train(
    learning_rate: float,
    hidden_size: int,
    agent: SnakeAgent,
    env: SnakeGameAI,
    num_cycles=100,
    width=640,
    height=480,
    speed=20,
    block_size=20,
):
    """_summary_
    The main training function which can be called to train the function

    Args:
        learning_rate (int)
        hidden_size (int):
    """
    try:
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        while num_cycles >= 0:
            state_old = agent.get_state(env)
            final_move = agent.get_action(state_old)

            reward, done, score = env.play_step(final_move)
            state_new = agent.get_state(env)

            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                env.reset_state()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                print("Game", agent.n_games, "Score", score, "Record:", record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
                num_cycles -= 1
    except Exception:
        raise TrainingException(func="train")


def save_model_as_pythorch(agent: SnakeAgent, directory: str):
    """Can be used t save the model as a pytorch binary

    Args:
        agent (SnakeAgent): Agent from class above
        directory (str): Directory to store the movel
    """
    model = agent.model
    model.save(f"{directory}_{agent.name}.pth")


# if __name__ == "__main__":
#     train()
