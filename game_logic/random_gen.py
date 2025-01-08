import random
from random import randint, choice
from game_logic.resource_manager import ResourceManager
import logging
import pprint

# configure logger
logging.basicConfig(level= logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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
        self.max_number = (n * 7)
        if self.n >= 8 or self.n < 2:
            raise ValueError(f"N-back needs to be between 2 and 8, Genius")

        self.n_back_max_number = self.max_number - self.n

        # Validate tab_coord dictionary
        try:
            self. tab_coords = ResourceManager.get_tablet_coords()
            if not self.tab_coords:
                raise ValueError(f"Tab_coordinate dictionary cannot be empty, Genius")
        except Exception as e:
            logger.error(f"Failed to initialise tab_coords dictionary: {e}")

    def random_list_generator(self):
        """Controller method that calls the other methods to generate two random lists. Both lists
        have repeated values using the same indices:
        n_back_num_list
        n_back_coord_list
        """
        # Get indices and random_sample_indices
        indices, random_sample_indices = self.random_index_generator()
        # Call create n_back methods with indices and random_sample_indices as arguments
        n_back_num_list = self.create_n_back_num_list(indices, random_sample_indices)
        n_back_coord_list = self.create_n_back_tab_coord_list(indices, random_sample_indices)
        return n_back_num_list, n_back_coord_list


    def random_index_generator(self):
        "max_number reduced by n value to allow for repeat on last index"
        # generate set for unique values and convert to list
        indices = list(set(i for i in range(0, self.n_back_max_number)))
        logger.debug(f"Before shuffle Indices: {indices}")
        random.shuffle(indices)
        # randomly sample shuffled indices to determine repeated number and coordinate locations in lists
        random_sample_indices = self.random_sample_indices(indices)
        logger.info(f"Shuffled indices: {indices}\nLength shuffled indices: {len(indices)}")
        return indices, random_sample_indices

    def random_sample_indices(self, indices):
        "k represents the number of repeats per game"
        if len(indices) < 5:
            raise ValueError(f"Indices too short for sampling unique values")
        random_sample_indices = random.sample(indices, k=5)
        logger.info(f"Random_sample_indices: {list(random_sample_indices)}")
        return random_sample_indices


    def create_n_back_num_list(self, indices, random_sample_indices):
        """Using random sample of indices create n-back list where values are copied with n-gap values at the indices"""
        num_list = [randint(1, 9) for _ in range(self.max_number)]
        n_back_num_list = num_list.copy()
        # call duplicate values to
        n_back_number_list = self.duplicate_values(n_back_num_list, random_sample_indices, self.n)
        logger.info(f"n_back_num_list: {n_back_num_list}\nN-back number list: {n_back_number_list}")
        return n_back_number_list

    def create_n_back_tab_coord_list(self, indices, random_sample_indices):
        # Create list of tablet coordinate values
        tab_coords_list = list(self.tab_coords.values())
        logger.info(f"Pre_shuffled tab coords: {tab_coords_list}")
        random.shuffle(tab_coords_list)
        logger.info(f"Shuffled tab coords: {tab_coords_list}")
        # Generate n-back tab coords list to same length as num list
        full_tab_coord_list = []
        for _ in range(self.max_number):
            full_tab_coord_list.append(choice(tab_coords_list))

        # duplicate values at sample indices + n_back
        n_back_tab_coord_list = full_tab_coord_list.copy()
        n_back_tab_coord_list = self.duplicate_values(n_back_tab_coord_list, random_sample_indices, self.n )
        logger.info(f"Full tab coord list: {full_tab_coord_list}\nLength full tab coord list: {len(full_tab_coord_list)}\n"
              f"n_back tab_coord_list: {n_back_tab_coord_list}\n"
              f"Length n_back_tab_coord_list: {len(n_back_tab_coord_list)}"
        )
        return n_back_tab_coord_list

    def duplicate_values(self, base_list, sample_indices, offset):
        """Helper function that duplicates elements in lists based on index values"""
        duplicated_list = base_list.copy()
        for index in sample_indices:
            if index + offset >= len(base_list):
                raise ValueError(f"Index {index} + offset {offset} exceeds list bounds")
            duplicated_list[index + offset] = base_list[index]
        return duplicated_list


    def generate_correct_responses(self, n_back_num_list, n_back_coord_list, n_back):

        """ Returns a dictionary of expected correct responses for easy comparison to player_responses:
        where expected_position_key is 'g' if position is a n_back repeat, else None;
        and expected_number_key is 'j' if number is a n_backrepeat, else None.
        """
        correct_responses = {}

        for i in range(len(n_back_num_list)):
            if i > n_back and n_back_coord_list[i] == n_back_coord_list[i - n_back]:
                expected_position_key = 'g'
            else:
                expected_position_key = None

            if i > n_back and n_back_num_list[i] == n_back_num_list[i - n_back]:
                expected_number_key = 'j'
            else:
                expected_number_key = None

            correct_responses[i] = {
                "number": n_back_num_list[i],
                "coord": n_back_coord_list[i],
                "expected_position_key": expected_position_key,
                "expected_number_key": expected_number_key
            }
        return correct_responses


if __name__ == "__main__":
    n = int(input("Enter n-back number: "))
    display_number_time = 1500
    rand = RandomGenerator(n)
    rand.random_index_generator()
    n_back_num_list, n_back_coord_list = rand.random_list_generator()

    correct_responses = rand.generate_correct_responses(n_back_num_list, n_back_coord_list, n)
    pprint.pprint(correct_responses)