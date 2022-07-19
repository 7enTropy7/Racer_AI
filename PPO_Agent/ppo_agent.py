from environment import RacerEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

env = RacerEnvironment(render=True)

# check_env(env, warn=True)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=200000)
model.save("racer")