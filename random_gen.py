import random

import pygame
from random import sample, randint
from resources import ResourceManager

def random_index_generator(max_number, n):
    max_num = max_number - n
    # generate set for unique values and convert to list
    indices = list(set(i for i in range(0, max_num)))

    print(f"Indices Set: {indices}")

    rand_indices = sample(indices, k=5)
    print(f"Random_indices: {list(rand_indices)}")

    # Call duplicate_number_at_index(indices, num_list)
    create_n_back_num_list(rand_indices)


def create_n_back_num_list(rand_indices):
    """Using random sample of indices create n-back list where values are copied with n-gap values at the indices"""
    num_list = [randint(1, 9) for _ in range(max_number)]
    print(f"Number list: {num_list}")
    duplicate_number_at_index(rand_indices, num_list)


def duplicate_number_at_index(rand_indices, num_list):
    n_back_num_list = num_list.copy()
    for index in rand_indices:
        # for num in num_list:
        n_back_num_list[index + n] = num_list[index]
    print(f"Num_list post_duplicate: {num_list}")
    tab_coord_list(max_number)


def tab_coord_list(max_number):
    tab_coords = ResourceManager.get_table_coords()
    rand_keys = [random.choice(list(tab_coords.keys()))for _ in range(max_number - n)]
    rand_tab_coords = {f"{i}": tab_coords[key] for i, key in enumerate(rand_keys)}
    print(f"rand_tab_coords: {rand_tab_coords}")



if __name__ == "__main__":

    max_number = int(input("Maximum number of sequence for n-back game? :=  "))
    n = int(input("Enter n-back number: "))
    random_index_generator(max_number,n)
