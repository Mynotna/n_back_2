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

    def __init__(self):
        self.n = n
        self.max_number = max_number
        self.n_back_max_number = max_number - self.n
        self. tab_coords = ResourceManager.get_tablet_coords()

    def random_index_generator(self, n, max_number):
        "max_number reduced by n value to allow for repeat on last index"
        # generate set for unique values and convert to list
        random_indices = list(set(i for i in range(0, self.max_number)))
        self.random_sample_indices(random_indices)
        print(f"Indices Set: {random_indices}")

    def random_sample_indices(self,random_indices):
        "k represents the number of repeats per game"
        random_sample_indices = sample(random_indices, k=5)
        print(f"Random_indices: {list(random_sample_indices)}")
        self.create_n_back_num_list(random_indices,random_sample_indices)


    def create_n_back_num_list(self, random_indices, random_sample_indices):
        """Using random sample of indices create n-back list where values are copied with n-gap values at the indices"""
        num_list = [randint(1, 9) for _ in range(self.max_number)]
        print(f"Number list: {num_list}")
        return num_list

    def create_n_back_tab_coord_list(self, random_indices, random_sample_indices):
        # Create list of tablet coordinate values
        tab_coords_list = list(self.tab_coords.values())
        random.shuffle(tab_coords_list)
        # Generate n-back tab coords list
        n_back_tab_coord_list = []
        for i in range(random_indices):
            n_back_tab_coord_list.append(choice(tab_coords_list))
        print(f"n-back tab coord list: {n_back_tab_coord_list}")
        return n_back_tab_coord_list


    # def duplicate_at_n_back_index(rand_indices):
    #     n_back_num_list = create_n_back_num_list(rand_indices)
    #     n_back_coord_list = create_n_back_tab_coord_list(rand_indices)
    #     # Create copies of lists
    #     n_back_num_list_copy = n_back_num_list.copy()
    #     n_back_coord_list_copy = n_back_coord_list.copy()
    #     print(f"n_back_num_list pre randomising: {n_back_num_list_copy}")
    #     print(f"n_back_coord_list pre randomising: {n_back_coord_list_copy}")
    #
    #     # Copy values at index to value n_back steps ahead
    #     for index in rand_indices:
    #         n_back_num_list_copy[index + n] = n_back_num_list[index]
    #         n_back_coord_list_copy[index + n] = n_back_coord_list[index]
    #     print(f"n_back_num_list post randomising: {n_back_num_list_copy}")
    #     print(f"n_back_coord_list post randomising: {n_back_coord_list_copy}")


if __name__ == "__main__":

    max_number = int(input("Maximum number of sequence for n-back game? :=  "))
    n = int(input("Enter n-back number: "))
    rand = RandomGenerator()
    rand.random_index_generator(max_number, n)