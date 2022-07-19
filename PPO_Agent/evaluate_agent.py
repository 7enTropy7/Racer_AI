from environment import RacerEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

env = RacerEnvironment(render=True, evaluate=True)

model = PPO.load("racer", env=env)

evaluate_policy(model, model.get_env(), n_eval_episodes=10)
