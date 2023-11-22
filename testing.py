from pyrlkit.agents.snake_agent_smarter import (
    create_env,
    create_model,
    train,
    save_model_as_pythorch,
)

model = create_model()
env = create_env()
train(agent=model, env=env, learning_rate=0.0000001, hidden_size=256, num_cycles=500)
save_model_as_pythorch(model, "output")
