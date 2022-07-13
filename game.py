import os
import pygame
from car import Car
from utils import generate_border_walls, generate_track_checkpoints, generate_track_walls

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Racer_AI")
        width = 1280
        height = 720
        self.screen_dims = (width, height)
        self.screen = pygame.display.set_mode((width, height))#, pygame.NOFRAME)
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        ppu = 8
        car = Car(x=10, y=10, ppu=ppu)
        walls = []
        walls.extend(generate_border_walls(self.screen_dims))
        walls.extend(generate_track_walls('walls.pkl'))

        checkpoints = []
        checkpoints.extend(generate_track_checkpoints('checkpoints.pkl'))

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            car.step(action=pressed, walls=walls, dt=dt)
            # print("Car state (L, C, R): ", car.state())
            
            checkpoint_collision_flag = car.checkpoint_collision(checkpoints[0])
            if checkpoint_collision_flag:
                print("Checkpoint collision!")
                checkpoints.pop(0)
                car.reward += 1
                if len(checkpoints) == 0:
                    print("You win!")
                    car.reward += 10
                    print("Total reward: ",car.reward)
                    self.exit = True

            self.screen.fill((0, 0, 0))

            for wall in walls:
                wall.draw(self.screen)

            for checkpoint in checkpoints:
                checkpoint.draw(self.screen)

            car.draw(self.screen)

            pygame.display.flip()


            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
