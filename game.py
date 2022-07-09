import os
import pygame
from math import copysign
from car import Car

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Racer_AI")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        ppu = 32
        car = Car(5, 15, ppu=ppu)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            car.step(action=pressed, dt=dt)

            self.screen.fill((0, 0, 0))

            car.draw(self.screen)

            pygame.display.flip()


            self.clock.tick(self.ticks)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
