from wall import Wall
import random

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

    return walls

def generate_track_walls(screen_dims):
    walls = []
    
    walls.append(Wall((0, 0), (screen_dims[0], 0)))
    walls.append(Wall((0, 0), (0, screen_dims[1])))
    walls.append(Wall((screen_dims[0], 0), (screen_dims[0], screen_dims[1])))
    walls.append(Wall((0, screen_dims[1]), (screen_dims[0], screen_dims[1])))
    
    # for i in range(3):
    #     start_x = random.randint(0, screen_dims[0])
    #     start_y = random.randint(0, screen_dims[1])
    #     end_x = random.randint(0, screen_dims[0])
    #     end_y = random.randint(0, screen_dims[1])
    #     walls.append(Wall((start_x, start_y), (end_x, end_y)))

    return walls