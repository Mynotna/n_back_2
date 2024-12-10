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









