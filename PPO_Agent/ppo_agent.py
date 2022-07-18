from environment import RacerEnvironment
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

env = RacerEnvironment(render=True)

# from stable_baselines3.common.env_checker import check_env

# check_env(env, warn=True)


# episodes = 1
# for episode in range(1, episodes+1):
#     state = env.reset()
#     done = False
#     score = 0 
    
#     while not done:
#         # env.render()
#         print(env.observation_space)
#         action = env.action_space.sample()
#         n_state, reward, done, info = env.step(action)
#         score+=reward
#     print('Episode:{} Score:{}'.format(episode, score))
# env.close()

model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=100000)
model.save("racer")
# evaluate_policy(model, env, n_eval_episodes=10, render=False)