import pygame as py  

# define constants  
WIDTH = 500  
HEIGHT = 500  
FPS = 200

# define colors  
BLACK = (0 , 0 , 0)  
GREEN = (0 , 255 , 0)

# initialize pygame and create screen  
py.init()  
screen = py.display.set_mode((WIDTH , HEIGHT))  
# for setting FPS  
clock = py.time.Clock()  

rot = 0  
rot_speed = .2  

# define a surface (RECTANGLE)  
image_orig = py.Surface((1 , 100))  
# for making transparent background while rotating an image  
image_orig.set_colorkey(BLACK)  
# fill the rectangle / surface with green color  
image_orig.fill(GREEN)  
# creating a copy of orignal image for smooth rotation  
image = image_orig.copy()  
image.set_colorkey(BLACK)  
# define rect for placing the rectangle at the desired position  
rect = image.get_rect()
x, y = py.mouse.get_pos()
rect.center = (x, y)  
# keep rotating the rectangle until running is set to False

running = True  
while running:  

    x, y = py.mouse.get_pos()
    # set FPS  
    clock.tick(FPS)  
    # clear the screen every time before drawing new objects  
    screen.fill(BLACK)  
    # check for the exit  
    for event in py.event.get():  
        if event.type == py.QUIT:  
            running = False

    # rotating the orignal image
    keys = py.key.get_pressed()
    if keys[py.K_a]:
        rot_speed = .2 
    if keys[py.K_d]:
        rot_speed = -.2 

    # defining angle of the rotation  
    rot = (rot + rot_speed) % 360  
    # rotating the orignal image
    image = py.transform.rotate(image_orig, rot)  
    rect = image.get_rect(center = (x, y))  
    # drawing the rotated rectangle to the screen  
    screen.blit(image, rect)  
    # flipping the display after drawing everything  
    py.display.flip()

py.quit() 