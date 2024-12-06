import random
import pygame
from random import sample, randint, choice
from resources import ResourceManager

class RandomGenerator:
    """ Generates random sequence of indices.
    Randomly samples the random indices.
    Sample used with random sequence to generate n_back indices.
    n-back indices used to generate:
        n_back_num_list
        n_back_coord_list
    """

    def __init__(self, n):
        self.n = n
        self.max_number = (n * 5) + 1
        if self.n >= 8:
            raise ValueError(f"N-back value too large, Genius")


        self.n_back_max_number = self.max_number - self.n

        # Validate tab_coord dictionary
        try:
            self. tab_coords = ResourceManager.get_tablet_coords()
            if not self.tab_coords:
                raise ValueError(f"Tab_coordinate dictionary cannot be empty, Genius")
        except Exception as e:
            raise RuntimeError(f"Failed to initialise tab_coords dictionary: {e}")

    def random_index_generator(self):
        "max_number reduced by n value to allow for repeat on last index"
        # generate set for unique values and convert to list
        indices = list(set(i for i in range(0, self.n_back_max_number)))
        print(f"Before shuffle Indices: {indices}")
        random.shuffle(indices)
        self.random_sample_indices(indices)
        print(f"Shuffled indices: {indices}\nLength shuffled indices: {len(indices)}")

    def random_sample_indices(self, indices):
        "k represents the number of repeats per game"
        if len(indices) < 5:
            raise ValueError(f"Indices too short for sampling unique values")
        random_sample_indices = random.sample(indices, k=5)
        print(f"Random_sample_indices: {list(random_sample_indices)}")
        # Call create_n_back_num_list and create_n_back_tab_coord_list
        self.create_n_back_num_list(indices,random_sample_indices)
        self.create_n_back_tab_coord_list(indices, random_sample_indices)


    def create_n_back_num_list(self, indices, random_sample_indices):
        """Using random sample of indices create n-back list where values are copied with n-gap values at the indices"""
        num_list = [randint(1, 9) for _ in range(self.max_number)]
        n_back_num_list = num_list.copy()
        # call duplicate values to
        n_back_number_list = self.duplicate_values(n_back_num_list, random_sample_indices, self.n)
        print(f"n_back_num_list: {n_back_num_list}\nN-back number list: {n_back_number_list}")
        return n_back_number_list

    def create_n_back_tab_coord_list(self, indices, random_sample_indices):
        # Create list of tablet coordinate values
        tab_coords_list = list(self.tab_coords.values())
        random.shuffle(tab_coords_list)
        # Generate n-back tab coords list to same length as num list
        full_tab_coord_list = []
        for _ in range(self.max_number):
            full_tab_coord_list.append(choice(tab_coords_list))

        # duplicate values at sample indices + n_back
        n_back_tab_coord_list = full_tab_coord_list.copy()
        n_back_tab_coord_list = self.duplicate_values(n_back_tab_coord_list, random_sample_indices, self.n )
        print(f"Full tab coord list: {full_tab_coord_list}\nLength full tab coord list: {len(full_tab_coord_list)}\n"
              f"n_back tab_coord_list: {n_back_tab_coord_list}\n"
              f"Length n_back_tab_coord_list: {len(n_back_tab_coord_list)}"
        )
        return n_back_tab_coord_list

    def duplicate_values(self, base_list, sample_indices, offset):
        duplicated_list = base_list.copy()
        for index in sample_indices:
            if index + offset >= len(base_list):
                raise ValueError(f"Index {index} + offset {offset} exceeds list bounds")
            duplicated_list[index + offset] = base_list[index]
        return duplicated_list

if __name__ == "__main__":


    n = int(input("Enter n-back number: "))
    rand = RandomGenerator(n)
    rand.random_index_generator()