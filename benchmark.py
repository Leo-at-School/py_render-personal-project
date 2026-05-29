import timeit
import random
import math

def function_1():
    pass

def function_2():
    pass

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
    #Edit stuff here
    functions: list[list["function reference", "parameters"]] = [
        [function_1, ],
        [function_2, ]
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

