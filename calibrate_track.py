import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
done = False
points = []

counter = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Clicked:', event.pos, counter)
            counter += 1
            points.append(event.pos)

    click = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()
    # print(click, mousex, mousey)

    screen.fill('gray12')
    
    pygame.draw.rect(screen, (255,0,0), (80,80,64,32), 3)

    for point in points:
        pygame.draw.circle(screen, (0,255,0), center=point, radius=5, width=5)
    
    pygame.display.flip()
    clock.tick(60)