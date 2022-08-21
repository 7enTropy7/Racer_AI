import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense #, Dropout, Activation, Flatten, Reshape
#from keras.utils import np_utils

num_rollouts = 20
expert_name = "Racer"
data_file = "Racer_20_data"
mean_rewards = []
stds = []
main_returns = []

task_data = load_task_data("data/" + data_file + ".pkl")
obs_data = np.array(task_data["observations"])
act_data = np.array(task_data["actions"])

act_data = act_data.reshape(act_data.shape[0], act_data.shape[2])


for j in range(5): #Dagger main loop
    print("Dagger Loop: ", j)
    print("obs_data.shape", obs_data.shape)
    
    #create a Feedforward network useing Keras
    
    model = Sequential()
    model.add(Dense(96, activation = "relu", input_shape = (obs_data.shape[1],)))
    model.add(Dense(96, activation = "relu"))
    model.add(Dense(96, activation = "relu"))
    model.add(Dense(act_data.shape[1], activation = "linear"))

    model.compile(loss = "mean_squared_error", optimizer = "adam", metrics=["accuracy"])
    model.fit(obs_data, act_data, batch_size = 64, epochs = 30, verbose = 0)
    model.save('models/' + expert_name + '_dagger_model.h5')
    
        
    env = gym.make(expert_name)
    max_steps = env.spec.timestep_limit

    returns = []
    new_observations = []
    new_actions = []
    for i in range(num_rollouts):
        print('iter', i)
        obs = env.reset()

        #print("obs.shape:", obs)
        done = False
        totalr = 0.
        steps = 0

        dagger_model = load_model('models/' + expert_name + '_dagger_model.h5')
        while not done:
            expert_action = policy_fn(obs[None,:])
            predicted_action = dagger_model.predict(obs[None, :], batch_size = 64, verbose = 0)
            
            new_observations.append(obs)
            new_actions.append(expert_action)
            
            obs, r, done, _ = env.step(predicted_action)
            totalr += r
            steps += 1
            #if args.render:
            #env.render()
            if steps % 100 == 0: print("%i/%i"%(steps, max_steps))
            if steps >= max_steps:
                break
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
    act_data = np.concatenate((act_data, np.array(new_actions.reshape(new_actions.shape[0], new_actions.shape[2]))))

