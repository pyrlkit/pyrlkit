from pyrlkit.agents import SnakeAgent
from pyrlkit.environments import SnakeGameAI
from pyrlkit.agents.snake_agent import train


def test_train():
    agent = SnakeAgent(learning_rate=0.001, hidden_size=32)
    mock_game = SnakeGameAI()
    initial_memory_length = len(agent.memory)

    num_cycles = 1
    train(
        learning_rate=0.001,
        hidden_size=128,
        agent=agent,
        env=mock_game,
        num_cycles=num_cycles,
    )

    assert agent.n_games == 2
    assert len(agent.memory) > initial_memory_length
