import os
import sys
import pygame
import math
from math import sin, radians, degrees, copysign, cos
from pygame.math import Vector2
from raycast import Raycast
from utils import rotate_point

class Car:
    def __init__(self, x, y, ppu=32, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.acceleration = 0.0
        self.steering = 0.0
        self.ppu = ppu

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "assets/car.png")
        self.car_image = pygame.image.load(image_path)

        self.ray_c = Raycast(startpoint=Vector2(0,0), direction='c')
        self.ray_l = Raycast(startpoint=Vector2(0,0), direction='l')
        self.ray_r = Raycast(startpoint=Vector2(0,0), direction='r')

        # Border Vertices of Car
        self.f_l = (self.position.x * self.ppu + (128/2), self.position.y * self.ppu - (64/2))
        self.f_r = (self.position.x * self.ppu + (128/2), self.position.y * self.ppu + (64/2))
        self.b_l = (self.position.x * self.ppu - (128/2), self.position.y * self.ppu - (64/2))
        self.b_r = (self.position.x * self.ppu - (128/2), self.position.y * self.ppu + (64/2))
        


    def step(self, action, walls, dt):
        if action[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif action[pygame.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif action[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if action[pygame.K_RIGHT]:
            self.steering -= 30 * dt
        elif action[pygame.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

        self.update(walls, dt)

        collision_flag = False
        for wall in walls:
            front_collision = self.check_collision(wall, self.f_l, self.f_r) #front
            back_collision = self.check_collision(wall, self.b_l, self.b_r) #back
            left_collision = self.check_collision(wall, self.f_l, self.b_l) #left
            right_collision = self.check_collision(wall, self.f_r, self.b_r) #right

            if(front_collision or back_collision or left_collision or right_collision):
                collision_flag = True
                break
        
        if collision_flag:
            print('Collision!')
            sys.exit(1)

    def update(self, walls, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        self.ray_c.step(car_raycast_startpoint=self.position * self.ppu, car_angle=self.angle, walls=walls)
        self.ray_l.step(car_raycast_startpoint=self.position * self.ppu, car_angle=self.angle, walls=walls)
        self.ray_r.step(car_raycast_startpoint=self.position * self.ppu, car_angle=self.angle, walls=walls)

        self.f_l = (self.position.x * self.ppu + (128/2), self.position.y * self.ppu - (64/2))
        self.f_r = (self.position.x * self.ppu + (128/2), self.position.y * self.ppu + (64/2))
        self.b_l = (self.position.x * self.ppu - (128/2), self.position.y * self.ppu - (64/2))
        self.b_r = (self.position.x * self.ppu - (128/2), self.position.y * self.ppu + (64/2))
    
        self.f_l = rotate_point(self.position * self.ppu, self.f_l, radians(-self.angle))
        self.f_r = rotate_point(self.position * self.ppu, self.f_r, radians(-self.angle))
        self.b_l = rotate_point(self.position * self.ppu, self.b_l, radians(-self.angle))
        self.b_r = rotate_point(self.position * self.ppu, self.b_r, radians(-self.angle))

    def check_collision(self, wall, line_startpoint, line_endpoint):
        x1 = line_startpoint[0]
        y1 = line_startpoint[1]
        x2 = line_endpoint[0]
        y2 = line_endpoint[1]
        
        x3 = wall.start_pos[0]
        y3 = wall.start_pos[1]
        x4 = wall.end_pos[0]
        y4 = wall.end_pos[1]

        if(x1 == x2): 
            return False

        if(x3 == x4):
            if((x3 > min(x1,x2) and x3 < max(x1,x2)) and (min(y3,y4) < min(y1,y2) and max(y3,y4) > max(y1,y2))):
                return True
            else:
                return False

        a1 = (y1-y2)/(x1-x2)  
        a2 = (y3-y4)/(x3-x4) 
        b1 = y1-a1*x1 
        b2 = y3-a2*x3 

        if (a1 == a2):
            return False  # Parallel segments

        xa = (b2 - b1) / (a1 - a2)

        if ((xa < max(min(x1,x2), min(x3,x4))) or
            (xa > min(max(x1,x2), max(x3,x4)))):
            return False  # intersection is out of bound
        else:
            return True


    def state(self):
        return [self.ray_l.ray_length, self.ray_c.ray_length, self.ray_r.ray_length]
    
    def draw(self, screen):
        self.ray_c.draw(screen)
        self.ray_l.draw(screen)
        self.ray_r.draw(screen)

        rotated_car = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated_car.get_rect()
        screen.blit(rotated_car, self.position * self.ppu - (rect.width / 2, rect.height / 2))

        pygame.draw.circle(screen, (0,255,0), center=self.f_l, radius=5, width=2)
        pygame.draw.circle(screen, (0,255,0), center=self.f_r, radius=5, width=2)
        pygame.draw.circle(screen, (0,255,0), center=self.b_l, radius=5, width=2)
        pygame.draw.circle(screen, (0,255,0), center=self.b_r, radius=5, width=2)
