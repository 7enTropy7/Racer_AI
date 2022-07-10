import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from raycast import Raycast

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

    def state(self):
        return [self.ray_l.ray_length, self.ray_c.ray_length, self.ray_r.ray_length]
    
    def draw(self, screen):
        self.ray_c.draw(screen)
        self.ray_l.draw(screen)
        self.ray_r.draw(screen)

        rotated = pygame.transform.rotate(self.car_image, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * self.ppu - (rect.width / 2, rect.height / 2))
        pygame.draw.rect(self.car_image, (255,0,0), [0, 0, 128, 64], 5)
