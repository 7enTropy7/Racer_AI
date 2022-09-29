from environment import RacerEnvironment
from stable_baselines3 import PPO
import pickle

env = RacerEnvironment(render=True, evaluate=True)

model = PPO.load("models/trained_ppo_agent/racer", env=env)

num_episodes = 12
obs_data = []
act_data = []

for i in range(num_episodes):
    print("New Episode")
    obs = env.reset()
    done = False
    episode_observation_data = []
    episode_action_data = []
    while not done:
        action, next_hidden_state = model.predict(obs)
        episode_observation_data.append(obs.tolist())
        episode_action_data.append(action.tolist())
        obs, reward, done, info = env.step(action)
        if 'done' in info.keys():
            obs_data.extend(episode_observation_data)
            act_data.extend(episode_action_data)
            print(info, done)

with open('models/trained_ppo_agent/env_obs_data.pkl', 'wb') as f:
    pickle.dump(obs_data, f)

with open('models/trained_ppo_agent/env_act_data.pkl', 'wb') as f:
    pickle.dump(act_data, f)