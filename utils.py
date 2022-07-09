from wall import Wall

def generate_border_walls(screen_dims):
    walls = []
    
    walls.append(Wall((0, 0), (screen_dims[0], 0)))
    walls.append(Wall((0, 0), (0, screen_dims[1])))
    walls.append(Wall((screen_dims[0], 0), (screen_dims[0], screen_dims[1])))
    walls.append(Wall((0, screen_dims[1]), (screen_dims[0], screen_dims[1])))

    return walls