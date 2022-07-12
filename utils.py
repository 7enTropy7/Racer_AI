from wall import Wall
import random
import math

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def generate_border_walls(screen_dims):
    walls = []
    
    walls.append(Wall((0, 0), (screen_dims[0], 0)))
    walls.append(Wall((0, 0), (0, screen_dims[1])))
    walls.append(Wall((screen_dims[0], 0), (screen_dims[0], screen_dims[1])))
    walls.append(Wall((0, screen_dims[1]), (screen_dims[0], screen_dims[1])))
    
    for i in range(3):
        start_x = random.randint(0, screen_dims[0])
        start_y = random.randint(0, screen_dims[1])
        end_x = random.randint(0, screen_dims[0])
        end_y = random.randint(0, screen_dims[1])
        walls.append(Wall((start_x, start_y), (end_x, end_y)))

    # walls.append(Wall((700, 200), (700, 500)))

    return walls

def generate_track_walls():
    walls = []
    
    # walls.append(Wall(start_pos=(80, 48), end_pos=(700, 48)))
    # walls.append(Wall(start_pos=(700, 200), end_pos=(700, 500)))

    
    return walls