"""
This file holds the methods used to render a 3d scene.

Notes:
- Variables in ALL CAPS are from a settings file, or they are a pygame constant
- Coordinate system: y-up (like minecraft!)
"""
#Standard libraries
import math

#3rd party libraries
import pygame as pg

#Files
from render_settings import *
import global_objects
import math_utils

#====================================================================================================#
#Draws the vertices of a mesh
def draw_meshes(mesh_group: list[tuple[tuple[float]]]) -> None:
    for mesh in mesh_group:
        mesh_color: tuple[int] = mesh[0]
        mesh_vertices: tuple[tuple[float]] = mesh[1]
        mesh_lines: tuple[tuple[int]] = mesh[2]
        
        screen_mesh: list[tuple[float]] = vertex_to_display(mesh_vertices)
        
        """
        screen_mesh = [
            (x1, y1, toggle1),
            (x2, y2, toggle2),
            ...
        ]
        """
        
        for x, y, toggle in screen_mesh:
            
            if toggle:
                draw_pixel((x, y), mesh_color)
        
        #Crude lines
        for index_1, index_2 in mesh_lines:
            point_data_1: tuple[int, bool] = screen_mesh[index_1]
            point_data_2: tuple[int, bool] = screen_mesh[index_2]
            
            point_1: tuple[int] = (point_data_1[X], point_data_1[Y])
            point_2: tuple[int] = (point_data_2[X], point_data_2[Y])
            toggle_1: bool = point_data_1[TOGGLE]
            toggle_2: bool = point_data_2[TOGGLE]
            
            if toggle_1 and toggle_2:
                draw_line(point_1, point_2, mesh_color)
        

"""
Notes:
- Subscripts a, b, and c denote the compnents of a vector
- Subscripts x, y, and z denote the compnents of a point
- A "*" used between 2 vectors signifies a dot product, otherwise its regular multiplication
- A "x" used between 2 vectors signifies a cross product
- ALL VECTORS (except the vertices) SHOULD BE NORMALIZED
- The function represented as R rotates a vector P about vector V by t degrees (P rotates clockwise around V when facing down the same direction V points):
    R(t, V, P) = V(V*P) + cos(t)(P - V(V*P)) + sin(t)(VxP)

Process:
    let P = some vertex
    let N = screen's normal vector
    let SX = screen's local x axis (normalized).
    let Z_neg = negative z axis (normalized).
    let X = positive global x axis (normalized).
    
  - Pre-step: Center all vertices (subtract the camera's point from the screen's point) and precalcualte other values
    
  - Step 1: cull if not within the player's frustum
    
  - Step 2: Rotate a vertex so it lies in the x-y plane only
        First, find the angle between the screen's normal vector and the negative z axis:
            theta1 = arccos(N*Z_neg) or theta = arccos(-N_c) *Note: The arguments aren't divided by the vectors' lengths because both should be normalized
        
        Second, the axis of rotation is found:
            A = (NxZ_neg)/||NxZ_neg||
        
        Lastly, the vertex is rotated by theta about the axis of rotation:
            P_new = R(theta1, A, P)
            
  - Step 3: Rotate the vertex about the negative z axis until its local x axis aligns with the global x axis:
        First, the angle between the screen's local x axis and the global x axis is found:
            theta2 = arccos(SX*X) or arccos(SX_x) *Note: The arguments aren't divided by the vectors' lengths because both should be normalized
            
        Lastly, the vertex is rotated by theta about the negative z axis:
            new vertex = R(theta2, Z_neg, P_new)
            
  - Step 4: Repeat steps 1, 2, adn 3 for all vertices.
"""
def vertex_to_display(vertices: tuple[tuple[float]]) -> tuple[tuple[int]]:
    camera_x: float; camera_y: float; camera_z: float
    camera_x, camera_y, camera_z = global_objects.player_data.camera_xyz
    
    screen_x: float; screen_y: float; screen_z: float
    screen_x, screen_y, screen_z = global_objects.player_data.screen_xyz
    
    screen_normal_a: float; screen_normal_b: float; screen_normal_c: float; screen_normal: float
    screen_normal_a, screen_normal_b, screen_normal_c = screen_normal = global_objects.player_data.screen_normal
    
    screen_x_axis: tuple[int] = global_objects.player_data.screen_x_axis
    
    #PRECOMPUTED VALUES
    camera_screen_difference_x: float = camera_x - screen_x
    camera_screen_difference_y: float = camera_y - screen_y
    camera_screen_difference_z: float = camera_z - screen_z
    
    t_numerator: float = screen_normal_a*camera_screen_difference_x + screen_normal_b*camera_screen_difference_y + screen_normal_c*camera_screen_difference_z
    
    #Angle between screen normal and global z axis
    angle_orient: float = math.acos(math_utils.dot_product_3d(screen_normal, AXIS_Z_NEGATIVE))
    
    #Axis of rotation for projected vertices
    axis_of_rotation_orient: tuple[float] = math_utils.normalize_3d(math_utils.cross_product_3d(screen_normal, AXIS_Z_NEGATIVE))
    
    #Screen's x axis after the vertices have been oriented
    screen_x_axis_oriented: tuple[float] = math_utils.normalize_3d(math_utils.quaternion_rotation(angle_orient, axis_of_rotation_orient, screen_x_axis))
    
    #Angle between screen's oriented x axis and global x axis
    angle_align: float = math.acos(math_utils.dot_product_3d(screen_x_axis_oriented, AXIS_X_POSITIVE))
    
    #The axis of rotation the screen's local oriented x axis rotates about to align with the global x axis
    #Note: This axis can only be the positive or negative z axis
    if (screen_x_axis_oriented != AXIS_X_POSITIVE):
        axis_of_rotation_align: tuple[float] = math_utils.normalize_3d(math_utils.cross_product_3d(screen_x_axis_oriented, AXIS_X_POSITIVE))
    else: #Prevent any zero vectors from the axes being the same
        axis_of_rotation_align: tuple[float] = AXIS_Z_POSITIVE
    
    display_mesh: list[tuple[tuple[float, bool]]] = []
    for x, y, z in vertices:
        x: float; y: float; z: float
        
        #Cull
        if frustum_cull((x, y, z)):
            display_mesh.append((0, 0, False))
            continue
        
        #PROJECT THE VERTEX TO THE SCREEN
        #Parametric factor
        t: float = t_numerator/(screen_normal_a*(camera_x - x) + screen_normal_b*(camera_y - y) + screen_normal_c*(camera_z - z))

        #Calculate where vertices will map to screens
        x_projected: float = camera_screen_difference_x + (x - camera_x)*t 
        y_projected: float = camera_screen_difference_y + (y - camera_y)*t 
        z_projected: float = camera_screen_difference_z + (z - camera_z)*t
        
        #ORIENT ALIGNED VERTEX WITH GLOBAL X-Y PLANE
        aligned_vertex = math_utils.quaternion_rotation(angle_orient, axis_of_rotation_orient, (x_projected, y_projected, z_projected))
        
        #ORIENT THE VERTEX SO THE LOCAL AND GLOBAL X AXES ARE THE SAME
        final_display_point: tuple[float] = math_utils.quaternion_rotation(angle_align, axis_of_rotation_align, aligned_vertex)
        display_mesh.append((math_utils.new_round(final_display_point[X]), math_utils.new_round(final_display_point[Y]), True))
    
    return display_mesh

#Check if a point is within the player's frustum (true: outside frustum, false: inside frustum)
def frustum_cull(point: tuple) -> bool:
    frustum_plane_normals: tuple[tuple[float]] = global_objects.player_data.frustum_plane_normals
    frustum_plane_points:  tuple[tuple[float]] = global_objects.player_data.frustum_plane_points
    camera_xyz:                   tuple[float] = global_objects.player_data.camera_xyz
    point_plane_comparisons:       list[float] = []
    
    for plane_index in range(len(frustum_plane_normals)):
        point_plane_comparisons.append(sum(frustum_plane_normals[plane_index][i]*(point[i] - frustum_plane_points[plane_index][i]) for i in range(3)))
    
    return not all(point_plane_comparisons[i] > 0 for i in range(len(point_plane_comparisons)))

#Draws pixel to the screen (origin centered in screen)
def draw_pixel(point: tuple[int], rgb: tuple[int]) -> None:
    x: int; y: int
    x, y = point

    #y is offset by 1 because y = 0 is off-screen, origin is centered
    pixel: object = pg.Rect((x*DISPLAY_SCALE + DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2 - (y + 1)*DISPLAY_SCALE, DISPLAY_SCALE, DISPLAY_SCALE))
    pg.draw.rect(global_objects.player_data.display, rgb, pixel)

#Draws a line (2D only)
def draw_line(point_1: tuple[float], point_2: tuple[float], rgb: tuple[int]) -> None:
    x1: float; y1: float
    x1: float; y1: float
    x1 , y1 = point_1
    x2 , y2 = point_2
    
    #Singular point
    if x1 == x2 and y1 == y2:
        draw_pixel(point_1, rgb)
        return
    
    #Vertical line
    elif x1 == x2:
        for y in range(min(y1, y2), max(y1, y2)):
            draw_pixel((x1, y), rgb)
        return
        
    #Horizontal line
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2)):
            draw_pixel((x, y1), rgb)
        return
    
    slope: float = (y1 - y2)/(x1 - x2)
    intercept: float = y1 - slope*x1
    
    if abs(slope) <= 1:
        x1, y1 = point_1 if point_1[X] < point_2[X] else point_2
        x2, y2 = point_2 if point_1[X] < point_2[X] else point_1
        
        for x_temp in range(x1, x2 + 1):
            y_temp = slope*x_temp + intercept
            draw_pixel((x_temp, y_temp), rgb)
            
    else:
        x1, y1 = point_1 if point_1[Y] < point_2[Y] else point_2
        x2, y2 = point_2 if point_1[Y] < point_2[Y] else point_1
        
        for y_temp in range(y1, y2 + 1):
            x_temp = (y_temp - intercept)/slope
            draw_pixel((x_temp, y_temp), rgb)

#Run a demo!         
def cube_demo(screen_points, mesh_color):
    #Top Square
    draw_line(screen_points[0], screen_points[1], mesh_color)
    draw_line(screen_points[1], screen_points[2], mesh_color)
    draw_line(screen_points[2], screen_points[3], mesh_color)
    draw_line(screen_points[3], screen_points[0], mesh_color)
    
    #Bottom Square
    draw_line(screen_points[4], screen_points[5], mesh_color)
    draw_line(screen_points[5], screen_points[6], mesh_color)
    draw_line(screen_points[6], screen_points[7], mesh_color)
    draw_line(screen_points[7], screen_points[4], mesh_color)
    
    #Connecting lines
    draw_line(screen_points[0], screen_points[4], mesh_color)
    draw_line(screen_points[1], screen_points[5], mesh_color)
    draw_line(screen_points[2], screen_points[6], mesh_color)
    draw_line(screen_points[3], screen_points[7], mesh_color)
    
