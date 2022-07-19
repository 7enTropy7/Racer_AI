from wall import Wall
import random
import math
import pickle as pkl
import pygame

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def generate_border_walls(screen_dims):
    walls = []
    
    walls.append(Wall((0, 0), (screen_dims[0], 0), color=pygame.Color('black')))
    walls.append(Wall((0, 0), (0, screen_dims[1]), color=pygame.Color('black')))
    walls.append(Wall((screen_dims[0], 0), (screen_dims[0], screen_dims[1]), color=pygame.Color('black')))
    walls.append(Wall((0, screen_dims[1]), (screen_dims[0], screen_dims[1]), color=pygame.Color('black')))
    
    return walls

def generate_track_walls(file_name):
    walls = pkl.load(open(file_name, 'rb'))
    return walls

def generate_track_checkpoints(file_name):
    checkpoints = pkl.load(open(file_name, 'rb'))
    return checkpoints