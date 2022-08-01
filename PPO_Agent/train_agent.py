import os
from platform import architecture

from environment import RacerEnvironment
from utils import SaveOnBestTrainingRewardCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

log_dir = "trained_agent/"
os.makedirs(log_dir, exist_ok=True)

env = RacerEnvironment(render=True)
env = Monitor(env, log_dir)

# check_env(env, warn=True)

if os.path.exists('trained_agent/racer.zip'):
    print("Loading existing model")
    model = PPO.load('trained_agent/racer.zip', env=env)
else:
    print("Training new model")
    model = PPO("MlpPolicy", env, verbose=1)

callback = SaveOnBestTrainingRewardCallback(check_freq=2048, log_dir=log_dir)

model.learn(total_timesteps=600000, callback=callback)
# model.save("trained_agent/racer")