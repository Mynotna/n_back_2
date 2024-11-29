class ScoreManager:
    def __init__(self, n_back):
        self.n_back = n_back
        self.generated_numbers = []
        self.generated_positions = []
        self.player_number_inputs = []
        self.player_position_inputs = []


    def add_generated_data(self, number, position):
        self.generated_numbers.append(number)
        self.generated_positions.append(position)

    def add_player_input(self, input_time, input_type):
        if input_type == 'number':
            self.player_number_inputs.append(input_time)
        elif input_type == 'position':
            self.player_position_inputs.append(input_time)


    def check_number_match(self):
        if len(self.generated_numbers) > self.n_back:
            return self.generated_numbers[-1] == self.generated_numbers[-(self.n_back +1)]
        return False


    def check_position_match(self):
        if len(self.generated_positions) > self.n_back:
            return self.generated_positions[-1] == self.generated_positions[-(self.n_back +1)]
        return False


    def check_missed_responses(self):
        missed_number = False
        missed_position = False

        # Check for missed number response
        if not self.player_number_inputs or self.player_number_inputs[-1] < self.generated_numbers[-1]:
            missed_number = True

        if not self.player_position_inputs or self.player_position_inputs[-1] < self.generated_positions[-1]:
            missed_position = True

        return missed_number, missed_position



