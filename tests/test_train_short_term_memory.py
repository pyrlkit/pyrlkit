from pyrlkit.agents import SnakeAgent


def test_train_short_memory():
    agent = SnakeAgent(learning_rate=0.001, hidden_size=32)
    state = [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1]
    action = [1, 0, 0]
    reward = 1
    next_state = [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
    done = False
    agent.train_short_memory(state, action, reward, next_state, done)

    assert len(agent.memory) == 0
