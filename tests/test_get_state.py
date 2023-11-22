from pyrlkit.agents import SnakeAgent
from pyrlkit.environments import SnakeGameAI


def test_get_state():
    agent = SnakeAgent(learning_rate=0.001, hidden_size=32)
    mock_game = SnakeGameAI()
    state = agent.get_state(mock_game)
    assert len(state) == 11  # Check the length of the state array
