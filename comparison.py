from FFT import *
from homeMadeDCT import *
import numpy as np
import time
import csv
if __name__ == "__main__":
    
    dimension_array = np.linspace(25, 700, num=4)
    time_array_library_dct = []
    time_array_my_dct = []

    for dimension in dimension_array:
        print("Calcolo dimensioni: " + str(dimension))
        matrix = np.random.rand(int(dimension), int(dimension))

        start_time = time.time()
        #print(start_time);
        solved_library_dct2 = get_2D_dct(matrix)
        end_time = time.time() - start_time;
        time_array_library_dct.append(end_time)
        #print(end_time);

        start_time = time.time()
        solved_my_dct2 = dct2_my_implementation(matrix)
        end_time = time.time() - start_time;
        time_array_my_dct.append(end_time)

    with open('data.csv', 'w') as w:
        writer = csv.writer(w, delimiter=';')
        writer.writerows(zip(dimension_array, time_array_library_dct,time_array_my_dct))
#        writer.writerows(zip(dimension_array, time_array_library_dct))