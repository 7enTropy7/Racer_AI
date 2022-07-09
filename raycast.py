import pygame
from pygame.math import Vector2

class Raycast:
    def __init__(self, startpoint, direction):
        self.startpoint = startpoint
        if direction == 'c':
            self.initial_endpoint = self.startpoint + Vector2(3000, 0)
        if direction == 'l':
            self.initial_endpoint = self.startpoint + Vector2(3000, -1800)
        if direction == 'r':
            self.initial_endpoint = self.startpoint + Vector2(3000, 1800)
        self.endpoint = None
        
    def step(self, car_raycast_startpoint, car_angle, walls):
        self.endpoint = car_raycast_startpoint + self.initial_endpoint.rotate(-car_angle)
        self.startpoint = car_raycast_startpoint


    def draw(self, screen):
        pygame.draw.line(screen, (0,125,255), self.startpoint, self.endpoint, 2)

    def check_collision(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.startpoint.x
        y3 = self.startpoint.y
        x4 = self.endpoint.x
        y4 = self.endpoint.y
    
        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None
        
        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            print(collidePos)
            return collidePos
