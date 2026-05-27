"""
Notes:
- Variables in ALL CAPS are from a settings file or are a pygame constant
"""
#Standard libraries
import math

#Files
from render_settings import *

#====================================================================================================#

#Manually round
#(Python rounds to nearest even integer in the case of a number ending in .5 rather than rounding up)
def new_round(num: float) -> int:
    #Always round up if number has a 5 in the first digit after the decimal
    if math.floor((num - math.floor(num))*10) == 5:
        num: int = int(math.ceil(num))
    
    #Round down
    else:
        num: int = int(math.floor(num))
    
    return num

#Transpose a matrix
def transpose(matrix: tuple[tuple[float]]) -> tuple[tuple[float]]:
    return ((matrix[y][x] for y in range(len(matrix))) for x in range(len(matrix[0])))

#Multiply two matrices. For matrices with larger dimensions
def large_matrix_multiply(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    #Transpose matrix_b so matrix_b_transposed's rows (matrix_b's columns) can be zipped with matrix_a's rows
    matrix_b_transposed: list[list[float]] = transpose(matrix_b)
    new_matrix: list[list[float]] = []
    
    #Loop through rows of matrix_a
    for new_row in matrix_a:
        new_matrix_row: list[float] = []
        
        #Create new_matrix's row. Loop through rows of matrix_b_transposed (columns of matrix_b)
        for new_column in matrix_b_transposed:
            new_value: float = 0
            
            #Compute each value of the row
            for matrix_a_value, matrix_b_value in zip(new_row, new_column):
                new_value += matrix_a_value * matrix_b_value
            
            new_matrix_row.append(new_value)
        
        new_matrix.append(new_matrix_row)
    
    return new_matrix
    
#Multiply two matrices. For matrices with smaller dimensions
def small_matrix_multiply(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    #Initialize empty matrix
    new_matrix: list[list[float]] = [[0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]
    
    #Multiply
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                new_matrix[i][j] += matrix_a[i][k]*matrix_b[k][j]
                
    return new_matrix

#Takes in 2 quaternions (quaternion t and quaternion s) and outputs quaternion q. ORDER MATTERS
def quaternion_multiplication(quaternion_t: list[float], quaternion_s: list[float]) -> list[float]:
    """
    Note: 
      - The general formula was derived from multiplying the following 2 4x4 matrix representations of quaternions:
            
            |t0 -t1 -t2 -t3|   |s0 -s1 -s2 -s3|
            |t1  t0 -t3 -t1|   |s1  s0 -s3 -s1|
            |t2  t3  t0  t2| * |s2  s3  s0  s2|
            |t3 -t2  t1  t0|   |s3 -s2  s1  s0|
            
        
    General formula of quaternion t (t0, t2, t3, t4) multiplied with quaternion s (s0, s1, s2, s3):

        |t0*s0 - t1*s1 - t2*s2 - t3*s3   -t0*s1 - t1*s0 - t2*s3 + t3*s2   -t0*s2 + t1*s3 - t2*s0 - t3*s1   -t0*s3 - t1*s2 + t2*s1 - t3*s0|
        |t0*s1 + t1*s0 + t2*s3 - t3*s2    t0*s0 - t1*s1 - t2*s2 - t3*s3   -t0*s3 - t1*s2 + t2*s1 - t3*s0    t0*s2 - t1*s3 + t2*s0 + t3*s1|
        |t0*s2 - t1*s3 + t2*s0 + t3*s1    t0*s3 + t1*s2 - t2*s1 + t3*s0    t0*s0 - t1*s1 - t2*s2 - t3*s3   -t0*s1 - t1*s0 - t2*s3 + t3*s2|
        |t0*s3 + t1*s2 - t2*s1 + t3*s0   -t0*s2 + t1*s3 - t2*s0 - t3*s1    t0*s1 + t1*s0 + t2*s3 - t3*s2    t0*s0 - t1*s1 - t2*s2 - t3*s3|
        
    
    To get the final components of the quaternion you take the first column vector of this new matrix:
    
        q0 = t0*s0 - t1*s1 - t2*s2 - t3*s3
        q1 = t0*s1 + t1*s0 + t2*s3 - t3*s2
        q2 = t0*s2 - t1*s3 + t2*s0 + t3*s1
        q3 = t0*s3 + t1*s2 - t2*s1 + t3*s0
    """
    t0: float; t1: float; t2: float; t3: float
    t0, t1, t2, t3 = quaternion_t
    
    s0: float; s1: float; s2: float; s3: float
    s0, s1, s2, s3 = quaternion_s

    #Quaternion t is the given quaternion multiplied by the point (q*p)
    #Quaternion s is quaternion t multiplied by the conjugate of the given quaternion (t*q_conjugate)
    q0: float = t0*s0 - t1*s1 - t2*s2 - t3*s3
    q1: float = t0*s1 + t1*s0 + t2*s3 - t3*s2
    q2: float = t0*s2 - t1*s3 + t2*s0 + t3*s1
    q3: float = t0*s3 + t1*s2 - t2*s1 + t3*s0

    return [q0, q1, q2, q3]

#Rotates a point about a vector by some radians. The point rotates clockwise relative to facing down the direction the vector points
#VECTOR SHOULD BE NORMALIZED (aka the axis of rotation should be normalized)
#The point retains its distance from the origin throughout the entire rotation (the "magnitude" of the point is unchanged)
def quaternion_rotation(angle: float, axis: tuple[float], point: tuple[float]) -> tuple[float]:
    """
    Note:
      - A "*" used between 2 vectors signifies a dot product, otherwise its regular multiplication
      - A "x" used between 2 vectors signifies a cross product
      - The general formula was derived from multiplying the following 3 4x4 quaternion matrices (the unit 
        quaternion times the point being rotated (represented as a quaternion) times the unit quaternion's 
        conjugate) taking the form q*p*p_conjugate. Then the first column vector is taken from the resulting matrix:
            
            | cos(t)   -sin(t)*a  -sin(t)*b  -sin(t)*c|   |0 -x -y -z|   | cos(t)     sin(t)*a   sin(t)*b   sin(t)*c|
            |sin(t)*a    cos(t)   -sin(t)*c  -sin(t)*b|   |x  0 -z -y|   |-sin(t)*a    cos(t)    sin(t)*c   sin(t)*b|
            |sin(t)*b   sin(t)*c    cos(t)    sin(t)*a| * |y  z  0  x| * |-sin(t)*b  -sin(t)*c    cos(t)   -sin(t)*a|
            |sin(t)*c  -sin(t)*b   sin(t)*a    cos(t) |   |z -y  x  0|   |-sin(t)*c   sin(t)*b  -sin(t)*a    cos(t) |
        
        
      - The first column vector is then decomposed into a sum of the vectors and scalars:
      
            The definition of the vectors and scalars are:
                axis of rotation (normalized): V = (a, b, c) 
                          point being rotated: P = (x, y, z)
                 angle rotated about the axis: t
                    
            General formula for rotating a point in 3D space:
                V(V*P) + cos(t)(P - V(V*P)) + sin(t)(VxP)
    
    
      - Expanding this you get the equations which rotate according to the right-hand rule:
            new_x = a(ax + by + cz) + cos(t)(x - a(ax + by + cz)) + sin(t)()
            new_y = b(ax + by + cz) + cos(t)(y - b(ax + by + cz)) + sin(t)()
            new_z = c(ax + by + cz) + cos(t)(z - c(ax + by + cz)) + sin(t)()
    """
    a: float; b: float; c: float
    a, b, c = axis[X], axis[Y], axis[Z]
    
    x: float; y: float; z: float
    x, y, z = point

    #Repeated variables
    v_dot_p: float = a*x + b*y + c*z
    a_times_dot_product: float = a*v_dot_p
    b_times_dot_product: float = b*v_dot_p
    c_times_dot_product: float = c*v_dot_p
    angle_sin: float = math.sin(angle)
    angle_cos: float = math.cos(angle)
    
    #The new x, y, and z coordinates are given with the equations:
    new_x: float = a_times_dot_product + angle_cos*(x - a_times_dot_product) + angle_sin*(b*z - c*y)
    new_y: float = b_times_dot_product + angle_cos*(y - b_times_dot_product) + angle_sin*(c*x - a*z)
    new_z: float = c_times_dot_product + angle_cos*(z - c_times_dot_product) + angle_sin*(a*y - b*x)
    
    return vector_round_3d((new_x, new_y, new_z))

#Normalize a 3D vector
def normalize_3d(vector: tuple[float]) -> tuple[float]:
    normalize = math.sqrt(vector[X]**2 + vector[Y]**2 + vector[Z]**2)
    
    x_component: float = vector[X]/normalize
    y_component: float = vector[Y]/normalize
    z_component: float = vector[Z]/normalize
    
    return vector_round_3d((x_component, y_component,z_component))

#Cross product of two vectors. ORDER MATTERS
def cross_product_3d(vector_1: tuple[float], vector_2: tuple[float]) -> tuple[float]:
    x_component: float = vector_1[Y]*vector_2[Z] - vector_1[Z]*vector_2[Y]
    y_component: float = vector_1[Z]*vector_2[X] - vector_1[X]*vector_2[Z]
    z_component: float = vector_1[X]*vector_2[Y] - vector_1[Y]*vector_2[X]
    
    return vector_round_3d((x_component, y_component, z_component))
    
#Cross product of two vectors
def dot_product_3d(vector_1: tuple[float], vector_2: tuple[float]) -> tuple[float]:
    return vector_1[X]*vector_2[X] + vector_1[Y]*vector_2[Y] + vector_1[Z]*vector_2[Z]

#Rounds a vector to 12 decimal places (prevent floating point errors)    
def vector_round_3d(vector: tuple[float]) -> tuple[float]:
    return tuple(round(element, MAX_ROUND) for element in vector)

def vector_scale_3d(vector: tuple[float], scale: int) -> tuple[float]:
    return (scale*vector[X], scale*vector[Y], scale*vector[Z])
