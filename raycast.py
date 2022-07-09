import pygame
from pygame.math import Vector2

class Raycast:
    def __init__(self, startpoint, direction):
        self.startpoint = startpoint
        
        if direction == 'c':
            self.initial_endpoint = self.startpoint + Vector2(300, 0)
        if direction == 'l':
            self.initial_endpoint = self.startpoint + Vector2(300, -180)
        if direction == 'r':
            self.initial_endpoint = self.startpoint + Vector2(300, 180)
        
        self.endpoint = None
        

    def step(self, car_raycast_startpoint, car_angle):
        self.endpoint = car_raycast_startpoint + self.initial_endpoint.rotate(-car_angle)
        self.startpoint = car_raycast_startpoint

    def draw(self, screen):
        pygame.draw.line(screen, (0,125,255), self.startpoint, self.endpoint, 2)
