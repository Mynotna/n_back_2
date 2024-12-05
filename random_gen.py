import random

import pygame
from random import sample, randint
from resources import ResourceManager

def random_index_generator(max_number, n):
    max_num = max_number - n
    # generate set for unique values and convert to list
    indices = list(set(i for i in range(0, max_num)))
    random_sample_indices(indices)

    print(f"Indices Set: {indices}")

def random_sample_indices(indices):
    rand_indices = sample(indices, k=5)
    print(f"Random_indices: {list(rand_indices)}")

    # Call duplicate_at_n_back_index
    duplicate_at_n_back_index(rand_indices)

def create_n_back_num_list(rand_indices):
    """Using random sample of indices create n-back list where values are copied with n-gap values at the indices"""
    num_list = [randint(1, 9) for _ in range(max_number)]
    print(f"Number list: {num_list}")
    return num_list

def create_n_back_tab_coord_list(rand_indices):
    # Get tablet_coords
    tab_coords = ResourceManager.get_tablet_coords()
    tab_coords_list = list(tab_coords.values())
    random.shuffle(tab_coords_list)
    return tab_coords_list


def duplicate_at_n_back_index(rand_indices):
    n_back_num_list = create_n_back_num_list(rand_indices)
    n_back_coord_list = create_n_back_tab_coord_list(rand_indices)
    # Create copies of lists
    n_back_num_list_copy = n_back_num_list.copy()
    n_back_coord_list_copy = n_back_coord_list.copy()
    print(f"n_back_num_list pre randomising: {n_back_num_list_copy}")
    print(f"n_back_coord_list pre randomising: {n_back_coord_list_copy}")

    # Copy values at index to value n_back steps ahead
    for index in rand_indices:
        n_back_num_list_copy[index + n] = n_back_num_list[index]
        n_back_coord_list_copy[index + n] = n_back_coord_list[index]
    print(f"n_back_num_list post randomising: {n_back_num_list_copy}")
    print(f"n_back_coord_list post randomising: {n_back_coord_list_copy}")


# def duplicate_coord_at_index(rand_indices, tab_coords_list):
#     n_back_coord_list = tab_coords_list.copy()
#     print(f"n_back_coord_lis pre duplicate: {n_back_coord_list}")
#     for index in rand_indices:
#         n_back_coord_list[index + n] = n_back_coord_list[index]
#     print(f"n_back_coord_list post duplicate: {n_back_coord_list}")


    # # rand_keys = [random.choice(list(tab_coords.keys()))for _ in range(max_number - n)]
    # # rand_tab_coords = {f"{i}": tab_coords[key] for i, key in enumerate(rand_keys)}
    # print(f"tab_coords_list: {tab_coords_list}\nrand_keys: {rand_keys}\nrand_tab_coords: {rand_tab_coords}")


if __name__ == "__main__":

    max_number = int(input("Maximum number of sequence for n-back game? :=  "))
    n = int(input("Enter n-back number: "))
    random_index_generator(max_number,n)
