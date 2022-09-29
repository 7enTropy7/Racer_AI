# Racer_AI

A 2D OpenAI Gym style environment that allows you to create custom racing tracks with checkpoints, and train a car to navigate through them. This environment can be used as a benchmark for various reinforcement learning algorithms and is compatible with Stable Baselines 3.

<div align="center">

|    |    |
|----------|:-------------:|
| Action Space |  Discrete(3) |
| Observation Shape | (12,) |
| Observation High | 1000 |
| Observation Low | 0 |

</div>

In this repo, we have trained a PPO agent using Stable Baselines 3 to navigate through various custom race tracks. We then utilized the trained expert agent to help a novice agent traverse a new track using imitation learning (the Dagger algorithm). 

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Calibrate a Custom Track

Our environment is highly customizable. The calibration feature allows you to design your very own racing track and add checkpoints that the car must sequentially pass through. 

```bash
python calibrate_track.py
```

### Car Position and Orientation

On running the above script, a pygame window will open up. Start off by defining where you want the car to spawn. This can be achieved by simply left-clicking on the desired location. Once the car is placed, it will point in the direction of the mouse cursor. The angular orientation can be finalized by pressing ```C``` on the keyboard.

![car](https://user-images.githubusercontent.com/36446402/193001124-2866bda4-4688-4468-8638-33222fb36643.gif)


### Drawing the Track

Next, we draw the borders of the race track. You can add marker points to the canvas using left-clicks. Walls will be formed between every consecutive set of marker points. The ```Space``` key can be used to undo the most recently added marker point.

![track_draw](https://user-images.githubusercontent.com/36446402/193001203-e96f68f9-cc4d-4e03-b7d6-b7520372518f.gif)


### Adding Checkpoints

Checkpoints are used by the agent to gain a sense of direction in which the track must be traversed. Checkpoints must be created across the track in the order that the car must pass through them. To add a checkpoint, simply right-click on 2 points across the width of the track. Note that the sequence of the checkpoints will be the order in which the car passes through them. Be kind to your agent and make sure that the checkpoints are placed in a way that the car can actually reach them. It is recommended to create a larger number of checkpoints across turning points in the track.

![checkpoint](https://user-images.githubusercontent.com/36446402/193001287-50996dd1-98f4-4b90-81d1-71ce7e3e3585.gif)


The ```Z``` key can be used to undo the most recently added checkpoint.

### Saving the Track

Once you are satisfied with the track, you can save it by pressing the ```S``` key. The track will be saved as a <b><i>.pkl</i></b> file in the ```tracks/training``` folder.

You can create as many tracks as you want. If any track needs to be used for evaluation rather than training, it's <b><i>.pkl</i></b> file should be moved to the ```tracks/testing``` folder.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Reinforcement Learning Agent

Now that the track is finalized, you can train the agent to navigate through it with your desired RL algorithm. 

We have used the Proximal Policy Optimization (PPO) algorithm from <b>Stable Baselines 3</b> to train our agent. 


### Training

```bash
python train_ppo_agent.py
```

![train_ppo](https://user-images.githubusercontent.com/36446402/193001414-412087be-4e2d-4e0d-8bc1-a97b6d5728ce.gif)


### Testing

```bash
python evaluate_ppo_agent.py
```

![test_ppo](https://user-images.githubusercontent.com/36446402/193001470-5715eadb-6d1d-4699-9de0-5a25aa1233fd.gif)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Imitation Learning Agent


DAgger (Dataset Aggregation) is an iterative policy training algorithm that trains a novice agent by dynamically aggregating trajectories and learning to mimic an expert agent's policy on those trajectories. In this case, the expert agent is the one that we trained using PPO. The main advantage of DAgger is that the expert teaches the learner how to recover from past mistakes.

### Training
Before we start training, an initial dataset of state-action pairs representing the expert policy must be generated. This can be done by running the following script.

```bash
python generate_expert_data.py
```

Now, we can train the novice agent using the DAgger algorithm on any custom track. Note that the following script uses the tracks in the ```tracks/testing``` folder.

```bash
python dagger.py
```

![dagger](https://user-images.githubusercontent.com/36446402/193001554-629475f6-eb28-4f28-9068-925c2e523f9e.gif)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

# Authors
* [**Anirudh Rajiv Menon**](https://github.com/axe76)
* [**Unnikrishnan Menon**](https://github.com/7enTropy7)

# License
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details