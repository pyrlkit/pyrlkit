from pyrlkit.environments.snake import SnakeGameHuman
import pygame

if __name__ == '__main__':
    env = SnakeGameHuman()
    
    while True:
        game_over, score = env.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()
