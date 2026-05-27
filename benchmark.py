import timeit
import random
import math

def function_1():
    pass
    
def function_2():
    pass

def benchmark_functions(*functions: list[list["function reference", "any parameters"]]) -> tuple[float]:
    function_reference_1: "function reference" = functions[0][0]
    function_reference_2: "function reference" = functions[1][0]
    function_1_arguments: list["parameters"] = functions[0][1:]
    function_2_arguments: list["parameters"] = functions[1][1:]
    
    iterations: int = 1000
    tests: int = 100
    average_1: list = []
    average_2: list = []
    equality_list: list = []

    #Find average runtimes and if the functions give the same output
    for _ in range(iterations):
        
        runtime_1 = timeit.timeit(lambda: function_reference_1(*function_1_arguments), number=tests)
        runtime_2 = timeit.timeit(lambda: function_reference_2(*function_2_arguments), number=tests)
        
        average_1.append(runtime_1)
        average_2.append(runtime_2)
        
        equality_list.append(function_reference_1(*function_1_arguments) == function_reference_2(*function_2_arguments))

    average_1: float = sum(average_1)/len(average_1)
    average_2: float = sum(average_2)/len(average_2)
    
    return (average_1, average_2, all(equality_list))

function_1_data: list["function reference", "parameters"] = [function_1, (3, 5, 6)]
function_2_data: list["function reference", "parameters"] = [function_2, (3, 5, 6)]

function_1_average, function_2_average, equality = benchmark_functions(function_1_data, function_2_data)

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