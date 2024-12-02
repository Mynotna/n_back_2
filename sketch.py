import random
from random import choices, shuffle


def n_back_index_generator(n):

    max_num = 35 - n
    # generate index list
    indices = [i for i in range(0, max_num)]
    print(f"Indices: {indices}")

    rand_indices = choices(indices, k=5 )
    print(f"Random_indices: {rand_indices}")

    # Call duplicate_number_at_index(indices, num_list)
    create_rand_num_list(rand_indices)


def create_rand_num_list(rand_indices):
    num_list = [random.randint(1, 9) for _ in range(35)]
    print(f"Number list: {num_list}")
    duplicate_number_at_index(rand_indices, num_list)



def duplicate_number_at_index(rand_indices, num_list):
    n_back_num_list = num_list.copy()
    for index in rand_indices:
        # for num in num_list:
        num_list[index + 2] = num_list[index]
    print(f"Num_list post_duplicate: {num_list}")



if __name__ == "__main__":
    n = 3
    n_back_index_generator(n)