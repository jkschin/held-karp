#!/usr/bin/python

import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count
from heldkarp import generate_image_pair, generate_coordinates

def generate_tuples(coords, train_input, train_output, i):
    subset = random.sample(coords, 20)
    return (coords, subset, train_input, train_output, i)

def main():
    start = timer()
    size = (512, 512, 3)
    size_name = "%dx%d" %(size[0], size[0])
    num_roads = 20
    roads_name = "%d" %num_roads
    train_input = os.path.join(size_name, roads_name, "train", "input")
    train_output = os.path.join(size_name, roads_name, "train", "output")
    test_input = os.path.join(size_name, roads_name, "test", "input")
    test_output = os.path.join(size_name, roads_name, "test", "output")
    if not os.path.exists(train_input):
        os.makedirs(train_input)
    if not os.path.exists(train_output):
        os.makedirs(train_output)

    random.seed(1)
    coords = generate_coordinates(num_roads)
    generate_image_pair(coords, subset, 0)

    print(f'starting computations on {cpu_count()} cores')

    values = [i for i in range(10)]

    # with Pool() as pool:
    #     res = pool.map(square, values)
    #     print(res)

    # end = timer()
    # print(f'elapsed time: {end - start}')

if __name__ == '__main__':
    main()

    