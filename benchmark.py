#Currently working on this file. I haven't ran it yet, so... idk if it works
#I'm still working on things too, so I havent even finished coding what I want to code

import timeit
import random
import math

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

#Transpose a matrix
def transpose(matrix: tuple[tuple[float]]) -> tuple[tuple[float]]:
    return tuple(tuple(matrix[y][x] for y in range(len(matrix))) for x in range(len(matrix[0])))

#Plus anymore functions :)
#====================================================================================================#

def benchmark_functions(functions: list[list["function reference", "any parameters"]]) -> list[list[float], bool]:
    iterations: int = 100
    tests: int = 10
    average_runtimes: list[list[floats]] = []
    results_list: list[any] = []
    
    for i, function_data in enumerate(functions):
        for iteration in range(iterations):
            function_reference: "function reference" = function_data[0]
            function_arguments: "parameters" = function_data[1:]
            
            runtime = timeit.timeit(lambda: function_reference(*function_arguments), number=tests)
            
            if iteration == 0:
                average_runtimes.append(runtime)
                results_list.append(function_reference(*function_arguments))
            else:
                average_runtimes[i] += runtime
                
        average_runtimes[i] /= iterations
    
    equality: bool = all(results_list[i] == results_list[0] for i in range(1, len(results_list)))
    
    return [average_runtimes, equality]

#====================================================================================================#

if __name__ == "__main__":
    length_1: int = random.randint(1, 30)
    length_2: int = random.randint(1, 30)
    random_matrix_a = [[random.randint(1, 9) for col in range(length_2)] for row in range(length_1)]
    random_matrix_b = [[random.randint(1, 9) for col in range(length_1)] for row in range(length_2)]
    
    for row in random_matrix_a:
        print(row)
    
    print()
    
    for row in random_matrix_b:
        print(row)
    
    print()
    
    #Edit stuff here
    functions: list[list["function reference", "parameters"]] = [
        [large_matrix_multiply, random_matrix_a, random_matrix_b],
        [small_matrix_multiply, random_matrix_a, random_matrix_b]
    ]
    
    average_runtimes: list[float]; equality: bool
    average_runtimes, equality = benchmark_functions(functions)
    
    fastest_average_runtime: float = min(average_runtimes)
    fastest_average_runtime_index: int = average_runtimes.index(fastest_average_runtime)
    
    print(f"Equality: {equality}")
    print(f"Fastest: {functions[fastest_average_runtime_index][0].__name__}")
    print("\nStats:")
    
    for i, function_data in enumerate(functions):
        function_name = function_data[0].__name__
        print(f"{function_name} time: {average_runtimes[i]}")

