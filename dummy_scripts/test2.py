import pygame

pygame.init()
screen = pygame.display.set_mode((300, 400))
rect = pygame.Rect((10, 20), (30, 50))
pygame.draw.rect(screen, pygame.Color('blue'), rect)

for line in (((1, 25), (200, 25)), ((1, 90), (200, 90))):
    collideline = rect.collideline(line)
    print('collideline =', collideline)

    pygame.draw.line(screen, pygame.Color('green'), line[0], line[1])

    if collideline:
        pygame.draw.line(screen, pygame.Color('red'), collideline[0],
                         collideline[1])

pygame.display.flip()
pygame.quit()