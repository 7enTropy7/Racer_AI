import pygame
import sys
import pickle as pkl
import os
import math

from wall import Wall
from checkpoint import Checkpoint

os.makedirs('tracks', exist_ok=True)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False
points = []
walls = []
checkpoint_points = []
checkpoints = []

ppu = 8
metadata = {}

car_image = pygame.image.load("assets/car.png").convert_alpha()
car_x = None
car_y = None
car_angle = 0
car_attributes_flag = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.MOUSEBUTTONDOWN and car_attributes_flag == False:
            car_x = event.pos[0]
            car_y = event.pos[1] 

        elif event.type == pygame.MOUSEBUTTONDOWN and car_attributes_flag == True:
            # print('Clicked:', event.pos, counter)
            if event.button == 1:
                # if event.pos[0] > car_x and event.pos[1] > car_y and event.pos[0] < car_x + 64 and event.pos[1] < car_y + 32:
                #     print('Cannot place point there: ', event.pos) 
                # else:
                points.append(event.pos)
                print('Added: ', points)
            elif event.button == 3:
                # if event.pos[0] > car_x and event.pos[1] > car_y and event.pos[0] < car_x + 64 and event.pos[1] < car_y + 32:
                #     print('Cannot place checkpoint there: ', event.pos) 
                # else:
                checkpoint_points.append(event.pos)
                print('Added Checkpoint point: ', checkpoint_points)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(points) > 0:
                    deleted_point = points.pop()
                    print('Deleted: ', deleted_point)
                    if len(walls) > 0:
                        for wall in walls:
                            if deleted_point in wall:
                                walls.remove(wall)

            elif event.key == pygame.K_z:
                if len(checkpoint_points) > 0:
                    deleted_point = checkpoint_points.pop()
                    print('Deleted: ', deleted_point)
                    if len(checkpoints) > 0:
                        for checkpoint in checkpoints:
                            if deleted_point in checkpoint:
                                checkpoints.remove(checkpoint)

            elif event.key == pygame.K_c:
                car_attributes_flag = True


            elif event.key == pygame.K_s:
                print('Saving...')
                if len(walls) > 0 and len(checkpoints) > 0:
                    wall_obj_array = []
                    for wall in walls:
                        wall_obj_array.append(Wall(wall[0], wall[1]))
                    checkpoint_obj_array = []
                    for checkpoint in checkpoints:
                        checkpoint_obj_array.append(Checkpoint(checkpoint[0], checkpoint[1]))

                    metadata['walls'] = wall_obj_array
                    metadata['checkpoints'] = checkpoint_obj_array
                    metadata['ppu'] = ppu
                    metadata['car_x'] = car_x
                    metadata['car_y'] = car_y
                    metadata['car_angle'] = car_angle

                    # metadata['car'] = Car(x=car_x/ppu, y=car_y/ppu, ppu=ppu, angle=car_angle)

                    track_id = len(os.listdir('tracks')) + 1
                    pkl.dump(metadata, open('tracks/metadata_{}.pkl'.format(track_id), 'wb'))
                    print('Track: {} Saved Successfully.'.format(track_id))

                    sys.exit(1)
                else:
                    print('Track Walls or Checkpoints missing. \nQuitting...')
                    sys.exit(1)


        walls = [[points[i],points[i+1]] for i in range(len(points)-1)]
        checkpoints = [[checkpoint_points[i],checkpoint_points[i+1]] for i in range(0, len(checkpoint_points)-1, 2)]



    click = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    # print(click, mousex, mousey)

    screen.fill('gray12')
    
    for point in points:
        pygame.draw.circle(screen, (255,255,0), center=point, radius=5, width=5)
    
    for checpoint_point in checkpoint_points:
        pygame.draw.circle(screen, (0,255,255), center=checpoint_point, radius=5, width=5)


    if walls is not None:
        for wall in walls:
            pygame.draw.line(screen, pygame.Color('aquamarine4'), start_pos=wall[0], end_pos=wall[1], width=3)

    if checkpoints is not None:
        for checkpoint in checkpoints:
            pygame.draw.line(screen, pygame.Color('green'), start_pos=checkpoint[0], end_pos=checkpoint[1], width=2)

    if car_x is not None and car_y is not None:
        if not car_attributes_flag:
            car_angle = -math.degrees(math.atan2(event.pos[1] - car_y, event.pos[0] - car_x))
        rotated_car = pygame.transform.rotate(car_image, car_angle)
        bounding_rect = rotated_car.get_rect()
        screen.blit(rotated_car, (car_x - bounding_rect.width/2, car_y - bounding_rect.height/2))


    pygame.display.flip()
    clock.tick(60)