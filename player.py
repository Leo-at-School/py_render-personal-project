"""
This file only holds the methods that are used on the Player_Data class. The acutal class is inside data.py.

Notes:
- Variables in ALL CAPS are from a settings file, or they are a pygame constant
- Coordinate system: y-up (like minecraft!)
"""
#Standard libraries
import math

#3rd party libraries
import pygame as pg

#Files
from player_settings import *
from render_settings import *
import global_objects
import math_utils

#====================================================================================================#

#Process inputs
def pygame_events() -> str:
    #Check if user has quit
    for event in pg.event.get():
        if event.type == pg.QUIT or global_objects.player_data.key[pg.K_ESCAPE]:
            return "Stop"
    
#Process movement keys
def move() -> list[float]:
    x: float; y: float; z: float
    x,        y,        z       = global_objects.player_data.camera_xyz
    
    #Vector used for forwards and backwards movement
    forward_backward_vector = math_utils.normalize_3d(math_utils.cross_product_3d(global_objects.player_data.screen_x_axis, AXIS_Y_NEGATIVE))
    
    if global_objects.player_data.key[pg.K_w]:
        x += PLAYER_SPEED*forward_backward_vector[X]
        z += PLAYER_SPEED*forward_backward_vector[Z]
        
    if global_objects.player_data.key[pg.K_s]:
        x -= PLAYER_SPEED*forward_backward_vector[X]
        z -= PLAYER_SPEED*forward_backward_vector[Z]
        
    if global_objects.player_data.key[pg.K_d]:
        x += PLAYER_SPEED*global_objects.player_data.screen_x_axis[X]
        z += PLAYER_SPEED*global_objects.player_data.screen_x_axis[Z]
        
    if global_objects.player_data.key[pg.K_a]:
        x -= PLAYER_SPEED*global_objects.player_data.screen_x_axis[X]
        z -= PLAYER_SPEED*global_objects.player_data.screen_x_axis[Z]
        
    if global_objects.player_data.key[pg.K_SPACE]:
        y += PLAYER_SPEED
        
    if global_objects.player_data.key[pg.K_LCTRL]:
        y -= PLAYER_SPEED
        
    return (x, y, z)

#Look around (with arrow keys)
def look(vector) -> list[float]:
    result_vector: tuple[float] = vector
    
    horizontal_axis_of_rotation: tuple[float] = AXIS_Y_NEGATIVE
    vertical_axis_of_rotation: tuple[float] = math_utils.normalize_3d((global_objects.player_data.screen_x_axis[0], 0, global_objects.player_data.screen_x_axis[2])) #The player's x axis projected onto the x-z plane
    
    if global_objects.player_data.key[pg.K_UP]:
        result_vector = math_utils.quaternion_rotation(PLAYER_ROTATION_SPEED, vertical_axis_of_rotation, vector)
    
    if global_objects.player_data.key[pg.K_DOWN]:
        result_vector = math_utils.quaternion_rotation(-PLAYER_ROTATION_SPEED, vertical_axis_of_rotation, vector)
    
    if global_objects.player_data.key[pg.K_RIGHT]:
        result_vector = math_utils.quaternion_rotation(PLAYER_ROTATION_SPEED, horizontal_axis_of_rotation, vector)
        
    if global_objects.player_data.key[pg.K_LEFT]:
        result_vector = math_utils.quaternion_rotation(-PLAYER_ROTATION_SPEED, horizontal_axis_of_rotation, vector)

    return result_vector
