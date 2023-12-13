from pyrlkit.environments import MazeGameHuman


maze_game = MazeGameHuman()
game_over = False
while not game_over:
    game_over, score = maze_game.play_step()
