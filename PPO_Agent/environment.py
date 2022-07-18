import os
import pygame
from car import Car
from utils import generate_border_walls, generate_track_checkpoints, generate_track_walls
import gym
import numpy as np
from gym import Env
from gym.spaces import Box, Discrete

class RacerEnvironment(Env):
    def __init__(self, render=False):
        super(RacerEnvironment, self).__init__()

        self.action_space = Discrete(5)
        self.observation_space = Box(low=0, high=1000, shape=(7,), dtype=np.float32)
        self.reward = 0
        self.render_flag = render
        
        self.ppu = 8

        self.timesteps = 0

        # Pygame stuff
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
        self.walls.extend(generate_track_walls('walls.pkl'))

        self.checkpoints = []
        self.checkpoints.extend(generate_track_checkpoints('checkpoints.pkl'))

        self.car = Car(x=10, y=10, ppu=self.ppu)

    def reset(self):
        # print('\nReset!\n')
        # self.clock = pygame.time.Clock()
        # self.dt = self.clock.get_time() / 100

        self.checkpoints = []
        self.checkpoints.extend(generate_track_checkpoints('checkpoints.pkl'))
        self.reward = 0
        self.car = Car(x=10, y=10, ppu=self.ppu)
        state = []
        state.extend(self.car.state())
        state.extend([self.checkpoints[0].state()[0], self.checkpoints[0].state()[1]])
        state.extend([self.car.position.x * self.ppu, self.car.position.y * self.ppu])
        state = np.array(state).astype(np.float32)
        self.done = False
        return state

    def get_state(self):
        state = []
        state.extend(self.car.state())
        state.extend([self.checkpoints[0].state()[0], self.checkpoints[0].state()[1]])
        state.extend([self.car.position.x * self.ppu, self.car.position.y * self.ppu])
        state = np.array(state).astype(float)
        return state

    def step(self, action):
        self.timesteps += 1

        self.dt = self.clock.get_time() / 100

        self.done, reward = self.car.step(action=action, walls=self.walls, dt=self.dt)
        # print(self.car.position.x * self.ppu, self.car.position.y * self.ppu)
        
        if self.timesteps % 1024 == 0:
            # print('Timesteps: ', self.timesteps)
            self.done = True

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
            reward = 2
            self.timesteps = 1
            if len(self.checkpoints) == 0:
                print("You win!")
                reward = 10
                self.done = True

        if not self.done:
            self.render()        
            self.clock.tick(self.ticks)

        else:
            self.reset()

        return self.get_state(), reward, self.done, {}

    def render(self):

        if self.render_flag:
            self.screen.fill((0, 0, 0))

            for wall in self.walls:
                wall.draw(self.screen)

            for checkpoint in self.checkpoints:
                checkpoint.draw(self.screen)

            self.car.draw(self.screen)

            pygame.display.flip()
