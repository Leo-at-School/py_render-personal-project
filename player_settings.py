"""
This file holds initial variables for the user

Notes:  
- Coordinate system: y-up (like minecraft!)
"""
#Standard libraries
import math

#Files
from render_settings import X, Y, Z, DISPLAY_WIDTH, DISPLAY_HEIGHT, DISPLAY_SCALE

#User
PLAYER_SPEED:                float = 0.01
PLAYER_ROTATION_SPEED:       float = 0.005 #Radians
PLAYER_ORIENTATION:   tuple[float] = (1, 0, 0) #Both the screen's normal vector and the camera's direction
PLAYER_XYZ:            list[float] = (-25, 0, 0)
PLAYER_X:                    float = PLAYER_XYZ[X]
PLAYER_Y:                    float = PLAYER_XYZ[Y]
PLAYER_Z:                    float = PLAYER_XYZ[Z]
PLAYER_HORIZONTAL_FOV:       float = math.pi/3
PLAYER_VERTICAL_FOV:         float = math.atan((DISPLAY_HEIGHT/DISPLAY_WIDTH)*math.tan(PLAYER_HORIZONTAL_FOV))
PLAYER_SCREEN_DISTANCE:        int = DISPLAY_WIDTH/(DISPLAY_SCALE*math.tan(PLAYER_HORIZONTAL_FOV))
PLAYER_SCREEN_XYZ:    tuple[float] = tuple(PLAYER_XYZ[i] + (PLAYER_ORIENTATION[i]*PLAYER_SCREEN_DISTANCE) for i in range(3))
PLAYER_SCREEN_X_AXIS: tuple[float] = (0, 0, 1)
