import pickle
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense #, Dropout, Activation, Flatten, Reshape
#from keras.utils import np_utils
from environment import RacerEnvironment
from stable_baselines3 import PPO

num_rollouts = 1
expert_name = "Racer"
data_file = "Racer_20_data"
mean_rewards = []
stds = []
main_returns = []

# task_data = load_task_data("data/" + data_file + ".pkl")
with open('trained_agent/env_obs_data.pkl', 'rb') as f:
    obs_data = pickle.load(f)

with open('trained_agent/env_act_data.pkl', 'rb') as f:
    act_data = pickle.load(f)

obs_data = np.array(obs_data) 
act_data = np.array(act_data)

# print(obs_data.shape)
# print(act_data.shape)

# act_data = act_data.reshape(act_data.shape[0], act_data.shape[2])


for j in range(5): #Dagger main loop
    print("Dagger Loop: ", j)
    print("obs_data.shape", obs_data.shape)
    
    #create a Feedforward network useing Keras
    
    model = Sequential()
    model.add(Dense(96, activation = "relu", input_shape = (obs_data.shape[1],)))
    model.add(Dense(96, activation = "relu"))
    model.add(Dense(96, activation = "relu"))
    model.add(Dense(3, activation = "softmax"))

    model.compile(loss = "sparse_categorical_crossentropy", optimizer = "adam", metrics=["accuracy"])
    model.fit(obs_data, act_data, batch_size = 64, epochs = 30, verbose = 0)
    model.save('dagger_models/' + expert_name + '_dagger_model.h5')
    
        
    env = RacerEnvironment(render=True)
    # max_steps = env.spec.timestep_limit
    
    expert_model = PPO.load("trained_agent/racer", env=env)

    returns = []
    new_observations = []
    new_actions = []
    for i in range(num_rollouts):
        print('iter', i)
        obs = env.reset()
        done = False
        totalr = 0.
        steps = 0

        dagger_model = load_model('dagger_models/' + expert_name + '_dagger_model.h5')
        while not done:
            expert_action, _next_hidden_state = expert_model.predict(obs)#policy_fn(obs[None,:])
            predicted_action = np.argmax(dagger_model.predict(obs[None, :], batch_size = 64, verbose = 0), axis=-1)[0]
            print("Predicted action: ", predicted_action)
            new_observations.append(obs)
            new_actions.append(expert_action)
            
            obs, r, done, _ = env.step(predicted_action)
            totalr += r
            steps += 1
        returns.append(totalr)

    print('returns', returns)
    print('mean return', np.mean(returns))
    print('std of return', np.std(returns))
    
    #record returns
    main_returns.append(returns)
    mean_rewards.append(np.mean(returns))
    stds.append(np.std(returns))
    
    #data aggregation
    obs_data = np.concatenate((obs_data, np.array(new_observations)))
    new_actions = np.array(new_actions)
    act_data = np.concatenate((act_data, new_actions))#np.array(new_actions.reshape(new_actions.shape[0], new_actions.shape[2]))))

