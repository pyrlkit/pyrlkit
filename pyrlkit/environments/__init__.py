import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .snake import SnakeGameAI, SnakeGameHuman
from .maze import MazeGameAI, MazeGameHuman
