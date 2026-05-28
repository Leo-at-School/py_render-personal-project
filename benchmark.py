#Currently working on this file. I haven't ran it yet, so... idk if it works
#I'm still working on things too, so I havent even finished coding what I want to code

import timeit
import random
import math

def function_1():
    pass
    
def function_2():
    pass

#Plus anymore functions :)

def benchmark_functions(*functions: list[list["function reference", "any parameters"]]) -> list[list[float], bool]:
    iterations: int = 1000
    tests: int = 10
    average_runtimes: list[list[floats]] = []
    results_list: list[any] = []
    equality: bool = false
    
    for i in range(len(functions))
        for iteration in range(iterations):
            function_reference: "function reference" = functions[i][0]
            function_arguments: "parameters" = functions[i][1:]
            runtime = timeit.timeit(lambda: function_reference(*function_arguments), number=tests)

            if iteration == 0:
                average_1.append(runtime)
                results_list.append(function_reference(*function_arguments))
            else:
                average_1 += runtime

    for i in range(len(average_runtimes)):
        average_runtimes /= iterations
    
    equality = len(set(results_list)) == 1
    
    return [average_runtimes, equality]

function_1_data: list["function reference", "parameters"] = [function_1, ]
function_2_data: list["function reference", "parameters"] = [function_2, ]

averages, equality = benchmark_functions(function_1_data, function_2_data)

#Store the variable name of the averages and the function name associated with that average
function_dict = {
"function_1_average": "function_1",
"function_2_average": "function_2"
}

print(f"function_1 time: {function_1_average}")
print(f"function_2 time: {function_2_average}")

fastest_average_num: float = min(function_1_average, function_2_average)

#Find the string representation of the fastest function
for index, key in enumerate(function_dict):
    #The value of the current average is grabbed from the globals() dictionary using the key in function_dict
    #This is then compared to the value of fastest_average_num
    if globals()[key] == fastest_average_num:
        fastest_average_name = key
        break
    
    if index == len(function_dict.keys()):
        fastest_average_name = "ERROR!!!"

print(f"Fastest: {function_dict[fastest_average_name]}")
print(f"Equality: {equality}")
