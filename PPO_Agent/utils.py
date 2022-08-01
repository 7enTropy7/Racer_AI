from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
import os
from wall import Wall
import math
import numpy as np
import pickle as pkl
import pygame

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def generate_border_walls(screen_dims):
    walls = []
    
    walls.append(Wall((0, 0), (screen_dims[0], 0), color=pygame.Color('black')))
    walls.append(Wall((0, 0), (0, screen_dims[1]), color=pygame.Color('black')))
    walls.append(Wall((screen_dims[0], 0), (screen_dims[0], screen_dims[1]), color=pygame.Color('black')))
    walls.append(Wall((0, screen_dims[1]), (screen_dims[0], screen_dims[1]), color=pygame.Color('black')))
    
    return walls

def generate_track_walls(file_name):
    walls = pkl.load(open(file_name, 'rb'))
    return walls

def generate_track_checkpoints(file_name):
    checkpoints = pkl.load(open(file_name, 'rb'))
    return checkpoints

class SaveOnBestTrainingRewardCallback(BaseCallback):
    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'racer')
        self.best_mean_reward = -np.inf

    # def _init_callback(self) -> None:
    #     if self.save_path is not None:
    #         os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:
            x, y = ts2xy(load_results(self.log_dir), 'timesteps')
            if len(x) > 0:
                mean_reward = np.mean(y[-100:])
                if self.verbose > 0:
                    print(f"Num timesteps: {self.num_timesteps}")
                    print(f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}")

                if mean_reward > self.best_mean_reward:
                    self.best_mean_reward = mean_reward
                    if self.verbose > 0:
                        print(f"Saving new best model to {self.save_path}")
                    self.model.save(self.save_path)

        return True