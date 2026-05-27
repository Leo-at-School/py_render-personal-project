"""
This file holds classes that only serve to hold information. The classes are initialized in global_objects.py.

Notes:
- Variables in ALL CAPS are from a settings file, or they are a pygame constant
- The only difference between the Static_Meshes and Dynamic_Meshes classes are that they group meshes based on how they should be treated. The classes are functionally the same.
"""
#Standard libraries
import math

#3rd party libraries
import pygame as pg

#Files
from player_settings import *
from render_settings import *
import math_utils

#====================================================================================================#
"""
Holds:
- Player's position and orientation
- Player's key presses
- The screen's position and orientation
- The display object (for rendering to the screen)

Notes:
- screen_xyz is also the player orientation
- the player's camera position is also the player's position
- screen_normal and screen_x_axis are guaranteed to be normalized
"""
class Player_Data:
    def __init__(self, display) -> None:
        self.camera_xyz:             tuple[float] = PLAYER_XYZ
        self.screen_xyz:             tuple[float] = PLAYER_SCREEN_XYZ
        self.screen_normal:          tuple[float] = math_utils.normalize_3d(PLAYER_ORIENTATION)
        self.screen_x_axis:          tuple[float] = math_utils.normalize_3d(PLAYER_SCREEN_X_AXIS)
        self.key:                     tuple[bool] = pg.key.get_pressed()
        self.display:                      object = display
        
        self.frustum_plane_normals: tuple[tuple[float]] = (
            math_utils.quaternion_rotation(PLAYER_VERTICAL_FOV, math_utils.normalize_3d(math_utils.cross_product_3d(self.screen_normal, self.screen_x_axis)), self.screen_normal),
            math_utils.quaternion_rotation(-PLAYER_VERTICAL_FOV, math_utils.normalize_3d(math_utils.cross_product_3d(self.screen_normal, self.screen_x_axis)), self.screen_normal),
            math_utils.quaternion_rotation(PLAYER_HORIZONTAL_FOV, self.screen_x_axis, self.screen_normal),
            math_utils.quaternion_rotation(-PLAYER_HORIZONTAL_FOV, self.screen_x_axis, self.screen_normal),
            self.screen_normal,
            math_utils.vector_scale_3d(self.screen_normal, -1)
        )
        self.frustum_plane_points: tuple[tuple[float]] = (
            self.camera_xyz,
            self.camera_xyz,
            self.camera_xyz,
            self.camera_xyz,
            tuple(self.camera_xyz[i] + MIN_RENDER_DISTANCE*self.screen_normal[i] for i in range(3)),
            tuple(self.camera_xyz[i] + MAX_RENDER_DISTANCE*self.screen_normal[i] for i in range(3))
        )
    
    def update_data(
        self,
        camera_xyz:    tuple[float],
        screen_xyz:    tuple[float],
        screen_normal: tuple[float],
        screen_x_axis: tuple[float],
        key:            tuple[bool],
        display:             object
    ) -> None:
        self.camera_xyz       = camera_xyz
        self.screen_xyz       = screen_xyz
        self.screen_normal    = math_utils.normalize_3d(screen_normal)
        self.screen_x_axis    = math_utils.normalize_3d(screen_x_axis)
        self.key              = key
        self.display          = display
        
        self.frustum_plane_normals: tuple[tuple[float]] = (
            math_utils.quaternion_rotation(PLAYER_VERTICAL_FOV, math_utils.normalize_3d(math_utils.cross_product_3d(self.screen_normal, self.screen_x_axis)), self.screen_normal),
            math_utils.quaternion_rotation(-PLAYER_VERTICAL_FOV, math_utils.normalize_3d(math_utils.cross_product_3d(self.screen_normal, self.screen_x_axis)), self.screen_normal),
            math_utils.quaternion_rotation(PLAYER_HORIZONTAL_FOV, self.screen_x_axis, self.screen_normal),
            math_utils.quaternion_rotation(-PLAYER_HORIZONTAL_FOV, self.screen_x_axis, self.screen_normal),
            self.screen_normal,
            math_utils.vector_scale_3d(self.screen_normal, -1)
        )
        self.frustum_plane_points: tuple[tuple[float]] = (
            self.camera_xyz,
            self.camera_xyz,
            self.camera_xyz,
            self.camera_xyz,
            tuple(self.camera_xyz[i] + MIN_RENDER_DISTANCE*self.screen_normal[i] for i in range(3)),
            tuple(self.camera_xyz[i] + MAX_RENDER_DISTANCE*self.screen_normal[i] for i in range(3))
        )

"""
Holds:
- Mesh groups
- A mesh's vertices
- Rules on how to connect the vertices

Notes:
- Static methods should not have any changes made to them
mesh_group structure:
    [                
        (rgb_1, (vertex_a1, vertex_a2, ...), (line_a1, line_a2, ...)), #Mesh 1
        (rgb_2, (vertex_b1, vertex_b2, ...), (line_b1, line_b2, ...)), #Mesh 2
        ...
    ]
- The tuple with elements labled as lines dictates how to connect 2 vertices (Eg. (0, 5) connects the vertices at index 0 and 5)
"""
class Static_Meshes:
    pass

"""
Holds:
- Mesh groups
- A mesh's vertices
- Rules on how to connect the vertices

Notes:
- Dynamic methods are allowed to have changes made to them
mesh_group structure:
    [                
        (rgb_1, (vertex_a1, vertex_a2, ...), (line_a1, line_a2, ...)), #Mesh 1
        (rgb_2, (vertex_b1, vertex_b2, ...), (line_b1, line_b2, ...)), #Mesh 2
        ...
    ]
- The tuple with elements labled as lines dictates how to connect 2 vertices (Eg. (0, 5) connects the vertices at index 0 and 5)
"""
class Dynamic_Meshes:
    pass
