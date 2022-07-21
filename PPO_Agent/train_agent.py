import os

from environment import RacerEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

env = RacerEnvironment(render=True)

# check_env(env, warn=True)

if os.path.exists('trained_agent/racer.zip'):
    model = PPO.load('trained_agent/racer.zip', env=env)
else:
    model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=100000)
model.save("trained_agent/racer")