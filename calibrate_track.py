from selectors import EVENT_WRITE
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False
points = []
walls = None
counter = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print('Clicked:', event.pos, counter)
            if event.pos[0] > 80 and event.pos[1] > 80 and event.pos[0] < 80 + 64 and event.pos[1] < 80 + 32:
                print('Cannot place point there: ', event.pos) 
            else:
                points.append(event.pos)
                print('Added: ', points)
                counter += 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                deleted_point = points.pop()
                print('Deleted: ', deleted_point)
                if len(walls) > 0:
                    for wall in walls:
                        if deleted_point in wall:
                            walls.remove(wall)
            if event.key == pygame.K_s:
                print('Saving...')
                walls = [[points[i],points[i+1]] for i in range(len(points)-1)]
                print(walls)


    click = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    # print(click, mousex, mousey)

    screen.fill('gray12')
    
    pygame.draw.rect(screen, (255,0,0), (80,80,64,32), 3)

    for point in points:
        pygame.draw.circle(screen, (0,255,0), center=point, radius=5, width=5)

    if walls is not None:
        for wall in walls:
            pygame.draw.line(screen, (255,255,255), start_pos=wall[0], end_pos=wall[1], width=3)
    
    pygame.display.flip()
    clock.tick(60)