from pyrlkit.agents import SnakeAgent


def test_get_action():
    agent = SnakeAgent(learning_rate=0.001, hidden_size=32)
    state = [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1]  # Example state
    action = agent.get_action(state)
    assert sum(action) == 1  # Check if only one action has been selected
