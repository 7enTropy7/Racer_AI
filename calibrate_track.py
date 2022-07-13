from selectors import EVENT_WRITE
import pygame
from wall import Wall
from checkpoint import Checkpoint
import sys
import pickle as pkl

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False
points = []
walls = []
checkpoint_points = []
checkpoints = []

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print('Clicked:', event.pos, counter)
            if event.button == 1:
                if event.pos[0] > 80 and event.pos[1] > 80 and event.pos[0] < 80 + 64 and event.pos[1] < 80 + 32:
                    print('Cannot place point there: ', event.pos) 
                else:
                    points.append(event.pos)
                    print('Added: ', points)
            elif event.button == 3:
                if event.pos[0] > 80 and event.pos[1] > 80 and event.pos[0] < 80 + 64 and event.pos[1] < 80 + 32:
                    print('Cannot place checkpoint there: ', event.pos) 
                else:
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

            elif event.key == pygame.K_s:
                print('Saving...')
                wall_obj_array = []
                for wall in walls:
                    wall_obj_array.append(Wall(wall[0], wall[1]))
                pkl.dump(wall_obj_array, open('walls.pkl', 'wb'))

                checkpoint_obj_array = []
                for checkpoint in checkpoints:
                    checkpoint_obj_array.append(Checkpoint(checkpoint[0], checkpoint[1]))
                pkl.dump(checkpoint_obj_array, open('checkpoints.pkl', 'wb'))

                sys.exit(1)

        walls = [[points[i],points[i+1]] for i in range(len(points)-1)]
        checkpoints = [[checkpoint_points[i],checkpoint_points[i+1]] for i in range(0, len(checkpoint_points)-1, 2)]



    click = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    # print(click, mousex, mousey)

    screen.fill('gray12')
    
    pygame.draw.rect(screen, (255,0,0), (80,80,64,32), 3)

    for point in points:
        pygame.draw.circle(screen, (255,255,0), center=point, radius=5, width=5)
    
    for checpoint_point in checkpoint_points:
        pygame.draw.circle(screen, (0,255,255), center=checpoint_point, radius=5, width=5)


    if walls is not None:
        for wall in walls:
            pygame.draw.line(screen, (255,255,255), start_pos=wall[0], end_pos=wall[1], width=3)

    if checkpoints is not None:
        for checkpoint in checkpoints:
            pygame.draw.line(screen, (0,255,0), start_pos=checkpoint[0], end_pos=checkpoint[1], width=3)

    pygame.display.flip()
    clock.tick(60)