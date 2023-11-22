from pyrlkit.agents.snake_agent import SnakeAgent


def test_remember():
    agent = SnakeAgent(learning_rate=0.001, hidden_size=32)
    state = [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1]
    action = [1, 0, 0]
    reward = 1
    next_state = [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
    done = False
    agent.remember(state, action, reward, next_state, done)
    assert len(agent.memory) == 1  # Check if the memory deque has stored the data
