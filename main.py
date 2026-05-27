"""
Notes:
- Variables in ALL CAPS are from a settings file, or they are a pygame constant
"""
#Standard libraries
import math
import random
import time

#3rd party libraries
import pygame as pg

#Files
from player_settings import *
from render_settings import *
import data
import global_objects
import math_utils
import player
import render

#====================================================================================================#

def main(
    camera_xyz:          list[float] = PLAYER_XYZ,
    screen_xyz:         tuple[float] = PLAYER_SCREEN_XYZ,
    screen_normal:      tuple[float] = math_utils.normalize_3d(PLAYER_ORIENTATION),
    screen_x_axis:      tuple[float] = math_utils.normalize_3d(PLAYER_SCREEN_X_AXIS)
) -> None:
    DISPLAY: object = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    global_objects.player_data: object = data.Player_Data(DISPLAY)
    global_objects.static_meshes: object = data.Static_Meshes()
    global_objects.dynamic_meshes: object = data.Dynamic_Meshes()
    
    while player.pygame_events() != "Stop":
        #PLAYER
        key = pg.key.get_pressed()
        
        camera_x: float; camera_y: float; camera_z: float; camera_xyz: tuple[float]
        camera_x,        camera_y,        camera_z       = camera_xyz              = player.move()
        
        screen_normal: tuple[float] = player.look(screen_normal)
        screen_xyz: tuple[float] = math_utils.vector_scale_3d(screen_normal, PLAYER_SCREEN_DISTANCE)
        
        screen_x_axis: tuple[float] = player.look(screen_x_axis)
        
        #==================================================#
        #DRAW
        
        render.draw_meshes(CUBE_DEMO_MESH)
        
        #==================================================#
        #UPDATE
        global_objects.player_data.update_data(camera_xyz, screen_xyz, screen_normal, screen_x_axis, key, DISPLAY)
        
        #Update screen before resetting the screen so the black screen gets overwritten in the next iteration (and doesnt draw on top of the current frame)
        pg.display.flip()
        DISPLAY.fill(COLOR_BLACK)

#====================================================================================================#

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
