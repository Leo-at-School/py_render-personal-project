"""
This file holds constants for the renderer
    
Notes:  
- Coordinate system: y-up (like minecraft!)
"""
#Misc
AXIS_X_POSITIVE:      tuple[float] = ( 1,  0,  0)
AXIS_Y_POSITIVE:      tuple[float] = ( 0,  1,  0)
AXIS_Z_POSITIVE:      tuple[float] = ( 0,  0,  1)
AXIS_X_NEGATIVE:      tuple[float] = (-1,  0,  0)
AXIS_Y_NEGATIVE:      tuple[float] = ( 0, -1,  0)
AXIS_Z_NEGATIVE:      tuple[float] = ( 0,  0, -1)
MAX_ROUND:                     int = 12 #The amount of decimal places vectors are rounded to

#Enhance readbility
X:                             int = 0 #Index for x values
Y:                             int = 1 #Index for y values
Z:                             int = 2 #Index for z values
TOGGLE:                        int = 2 #Index for the boolean value that toggles points on the screen
#==================================================#
#Screen
DISPLAY_WIDTH:                 int = 1200
DISPLAY_HEIGHT:                int = 800
DISPLAY_SCALE:                 int = 1 #Must be a common factor of the display's width and height
DISPLAY_SCALED_WIDTH:        float = DISPLAY_WIDTH/DISPLAY_SCALE
DISPLAY_SCALED_HEIGHT:       float = DISPLAY_HEIGHT/DISPLAY_SCALE
MAX_RENDER_DISTANCE:         float = 100
MIN_RENDER_DISTANCE:         float = 0.5

#==================================================#
#Colors
COLOR_WHITE:            tuple[int] = (255, 255, 255)
COLOR_GRAY:             tuple[int] = (128, 128, 128)
COLOR_GREY:             tuple[int] = (128, 128, 128)
COLOR_BLACK:            tuple[int] = (0  , 0  , 0  )
COLOR_PINK:             tuple[int] = (255, 0  , 255)
COLOR_RED:              tuple[int] = (255, 0  , 0  )
COLOR_ORANGE:           tuple[int] = (255, 128, 0  )
COLOR_YELLOW:           tuple[int] = (255, 255, 0  )
COLOR_GREEN:            tuple[int] = (0  , 255, 0  )
COLOR_CYAN:             tuple[int] = (0  , 255, 255)
COLOR_BLUE:             tuple[int] = (0  , 0  , 255)
COLOR_PURPLE:           tuple[int] = (128, 0  , 255)
COLOR_LIST:     list[tuple[float]] = [
                                     COLOR_BLACK,
                                     COLOR_GRAY,
                                     COLOR_WHITE,
                                     COLOR_PINK,
                                     COLOR_RED,
                                     COLOR_ORANGE,
                                     COLOR_YELLOW,
                                     COLOR_GREEN,
                                     COLOR_CYAN,
                                     COLOR_BLUE,
                                     COLOR_PURPLE
                                     ]

#==================================================#
#Demo meshes
CUBE_DEMO_MESH: list[tuple[tuple[int]]] = [
    (COLOR_WHITE,  ((-1,  1, -1), ( 1,  1, -1), ( 1,  1,  1), (-1,  1,  1), (-1, -1, -1), ( 1, -1, -1), ( 1, -1,  1), (-1, -1,  1)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Middle cube

    (COLOR_ORANGE, ((-5,  1, -1), (-3,  1, -1), (-3,  1,  1), (-5,  1,  1), (-5, -1, -1), (-3, -1, -1), (-3, -1,  1), (-5, -1,  1)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Front cube
    (COLOR_YELLOW, (( 3,  1, -1), ( 5,  1, -1), ( 5,  1,  1), ( 3,  1,  1), ( 3, -1, -1), ( 5, -1, -1), ( 5, -1,  1), ( 3, -1,  1)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Back cube

    (COLOR_BLUE,   ((-1,  5, -1), ( 1,  5, -1), ( 1,  5,  1), (-1,  5,  1), (-1,  3, -1), ( 1,  3, -1), ( 1,  3,  1), (-1,  3,  1)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Top cube
    (COLOR_GREEN,  ((-1, -3, -1), ( 1, -3, -1), ( 1, -3,  1), (-1, -3,  1), (-1, -5, -1), ( 1, -5, -1), ( 1, -5,  1), (-1, -5,  1)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Bottom cube

    (COLOR_PURPLE, ((-1,  1, -5), ( 1,  1, -5), ( 1,  1, -3), (-1,  1, -3), (-1, -1, -5), ( 1, -1, -5), ( 1, -1, -3), (-1, -1, -3)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))), #Left cube
    (COLOR_RED,    ((-1,  1,  3), ( 1,  1,  3), ( 1,  1,  5), (-1,  1,  5), (-1, -1,  3), ( 1, -1,  3), ( 1, -1,  5), (-1, -1,  5)), ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)))  #Right cube
]
