from FFT import *
from homeMadeDCT import *
import numpy as np
import time
import csv
if __name__ == "__main__":
    dimension_array = np.linspace(25, 700, num=28)
    time_array_library_dct = []
    time_array_my_dct = []
    for dimension in dimension_array:
        print("Computing the dimension: " + str(dimension))
        matrix = np.random.rand(int(dimension), int(dimension))
        start_time = time.time()
        solved_library_dct2 = get_2D_dct(matrix)
        time_array_library_dct.append(time.time() - start_time)
        start_time = time.time()
        solved_my_dct2 = dct2_my_implementation(matrix)
        time_array_my_dct.append(time.time() - start_time)
    with open('data.txt', 'w') as w:
        writer = csv.writer(w, delimiter='\t')
        writer.writerows(zip(dimension_array, time_array_library_dct,
        time_array_my_dct))