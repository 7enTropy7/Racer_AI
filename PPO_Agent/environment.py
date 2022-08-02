import os
import pickle as pkl
import random
import math
import pygame
from car import Car
from utils import generate_border_walls, generate_track_checkpoints, generate_track_walls
import gym
import numpy as np
from gym import Env
from gym.spaces import Box, Discrete

class RacerEnvironment(Env):
    def __init__(self, render=False, evaluate=False):
        super(RacerEnvironment, self).__init__()

        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=1000, shape=(12,), dtype=np.float32)
        self.reward = 0
        self.render_flag = render
        self.evaluate_flag = evaluate
        
        self.tracks = os.listdir('tracks')
        self.metadata = pkl.load(open('tracks/'+random.choice(self.tracks),'rb'))

        self.ppu = self.metadata['ppu']

        self.timesteps = 0

        pygame.init()

        width = 1280
        height = 720
        if self.render_flag:
            pygame.display.set_caption("Racer_AI")
            self.screen = pygame.display.set_mode((width, height))#, pygame.NOFRAME)

        self.screen_dims = (width, height)        
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.done = False
        # self.dt = self.clock.get_time() / 100

        self.walls = []
        self.walls.extend(generate_border_walls(self.screen_dims))
        self.walls.extend(self.metadata['walls'])

        self.checkpoints = []
        self.checkpoints.extend(self.metadata['checkpoints'])

        self.car = Car(x=self.metadata['car_x']/self.metadata['ppu'], y=self.metadata['car_y']/self.metadata['ppu'], ppu=self.ppu, angle=self.metadata['car_angle'], screen_width=width, screen_height=height)

        self.track_counter = 1

    def reset(self):
        self.metadata = pkl.load(open('tracks/'+'metadata_{}.pkl'.format(self.track_counter),'rb'))
        self.walls = []
        self.walls.extend(generate_border_walls(self.screen_dims))
        self.walls.extend(self.metadata['walls'])
        self.checkpoints = []
        self.checkpoints.extend(self.metadata['checkpoints'])
        self.reward = 0
        self.car = Car(x=self.metadata['car_x']/self.metadata['ppu'], y=self.metadata['car_y']/self.metadata['ppu'], ppu=self.ppu, angle=self.metadata['car_angle'])
        state = []
        state.extend(self.car.state())
        state.extend([self.checkpoints[0].state()[0], self.checkpoints[0].state()[1]])
        state.extend([self.car.position.x * self.ppu, self.car.position.y * self.ppu])
        # nearest_checkpoint_normalized_distance = math.sqrt(((self.car.position.x * self.ppu) - self.checkpoints[0].state()[0]) ** 2 + ((self.car.position.y * self.ppu) - self.checkpoints[0].state()[1]) ** 2) / math.sqrt(self.screen_dims[0]**2 + self.screen_dims[1]**2)
        # state.extend([nearest_checkpoint_normalized_distance])
        state = np.array(state).astype(np.float32)
        self.done = False

        self.track_counter += 1
        if self.track_counter > len(self.tracks):
            self.track_counter = 1
        return state

    def get_state(self):
        state = []
        state.extend(self.car.state())
        state.extend([self.checkpoints[0].state()[0]/self.screen_dims[0], self.checkpoints[0].state()[1]/self.screen_dims[1]])
        state.extend([(self.car.position.x * self.ppu)/self.screen_dims[0], (self.car.position.y * self.ppu)/self.screen_dims[1]])
        # nearest_checkpoint_normalized_distance = math.sqrt(((self.car.position.x * self.ppu) - self.checkpoints[0].state()[0]) ** 2 + ((self.car.position.y * self.ppu) - self.checkpoints[0].state()[1]) ** 2) / math.sqrt(self.screen_dims[0]**2 + self.screen_dims[1]**2)
        # state.extend([nearest_checkpoint_normalized_distance])
        state = np.array(state).astype(float)
        return state

    def step(self, action):
        self.timesteps += 1

        self.dt = self.clock.get_time() / 200

        self.done, reward = self.car.step(action=action, walls=self.walls, dt=self.dt)
        
        if self.timesteps % (1024//2) == 0:
            self.done = True
            reward -= 5

        # nearest_checkpoint_normalized_distance = math.sqrt(((self.car.position.x * self.ppu) - self.checkpoints[0].state()[0]) ** 2 + ((self.car.position.y * self.ppu) - self.checkpoints[0].state()[1]) ** 2) / math.sqrt(self.screen_dims[0]**2 + self.screen_dims[1]**2)
        # reward += (1-nearest_checkpoint_normalized_distance) * 0.1
        # print('reward: {}'.format(reward))

        if self.done:
            self.reward = reward
            state = self.get_state()

            self.render()        
            self.clock.tick(self.ticks)
            
            return state, self.reward, self.done, {}

        checkpoint_collision_flag = self.car.checkpoint_collision(self.checkpoints[0])
        if checkpoint_collision_flag:
            # print("Checkpoint!")
            self.checkpoints.pop(0)
            reward = 10
            self.timesteps = 1
            if len(self.checkpoints) == 0:
                print("You win!")
                reward = 20
                self.done = True

        if not self.done:
            self.render()        
            self.clock.tick(self.ticks)

        else:
            self.reset()

        return self.get_state(), reward, self.done, {}

    def render(self):

        if self.render_flag:
            pygame.event.get()
            self.screen.fill((0, 0, 0))

            for wall in self.walls:
                wall.draw(self.screen)

            if not self.evaluate_flag:
                for checkpoint in self.checkpoints:
                    checkpoint.draw(self.screen)

            self.car.draw(self.screen, self.evaluate_flag)

            pygame.display.flip()
