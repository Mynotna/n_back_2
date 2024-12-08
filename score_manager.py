import json

class ScoreManager:
    def __init__(self, n_back, n_back_num_list, n_back_coord_list):
        self.n_back = n_back
        self.n_back_num_list = n_back_num_list
        self.n_back_coord_list = n_back_coord_list
        self.player_number_inputs = []
        self.player_position_inputs = []


    def player_inputs(self, player_response, response_type):
        if response_type == "number":
            self.player_number_inputs.append(player_response)
        elif response_type == "position":
            self.player_number_inputs.append(player_response)


    def evaluate_responsed(self, index):
        # Check if the player made a response for number
        if index < len(self.player_number_inputs):
            if self.n_back_num_list[index] == self.player_inputs[index]:
                number_status = "correct"
            else:
                number_status = "incorrect"

        # Check if the player made a response for position
        if index < len(self.player_position_inputs):
            if self.n_back_coord_list == self.player_position_inputs:
                position_status = "correct"
            else:
                position_status = "incorrect"

        return number_status, position_status





    #
    # def add_player_input(self, input_time, input_type):
    #     if input_type == 'number':
    #         self.player_number_inputs.append(input_time)
    #     elif input_type == 'position':
    #         self.player_position_inputs.append(input_time)
    #
    #
    # def check_number_match(self):
    #     if len(self.generated_numbers) > self.n_back:
    #         return self.generated_numbers[-1] == self.generated_numbers[-(self.n_back +1)]
    #     return False
    #
    #
    # def check_position_match(self):
    #     if len(self.generated_positions) > self.n_back:
    #         return self.generated_positions[-1] == self.generated_positions[-(self.n_back +1)]
    #     return False
    #
    #
    # def check_missed_responses(self):
    #     missed_number = False
    #     missed_position = False
    #
    #     # Check for missed number response
    #     if not self.player_number_inputs or self.player_number_inputs[-1] < self.generated_numbers[-1]:
    #         missed_number = True
    #
    #     if not self.player_position_inputs or self.player_position_inputs[-1] < self.generated_positions[-1]:
    #         missed_position = True
    #
    #     return missed_number, missed_position



