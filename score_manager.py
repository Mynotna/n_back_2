import json

class ScoreManager:
    def __init__(self, player_responses, correct_responses):

        """The ScoreManager receives a dictionary (self.player_responses) from GamePlayState,
        and a correct_responses dictionary from RandomGenerator class and compares the two. They both should have
        exactly the same format for comparison and scoring, i.e.
        {
        0: (None, None),
        1: (j, None),
        2: (None, g)
        ditto
        }
        """
        # Initialise player_responses dictionary from GamePlayState class
        self.player_responses = player_responses
        # Initialise correct_responses dictionary from Random_gen class
        self.correct_responses = correct_responses


    def classify_key(self, expected, actual):
        """ Sorts a single key comparison:
        expected or actual are either None, 'g', or 'j'
        Returns: 'correct', 'missed', 'incorrect'.
        """
        if expected == actual:
            return 'correct'
        elif expected is None and actual is not None:
            return 'incorrect'
        elif expected is not None and actual is None:
            return 'missed'
        else:
            return 'incorrect'
    def evaluate_score(self):
       """This evaluates the player's score by comparing two dictionaries, one from the GamePlayState (player_responses),
       the other from RandomGenerator (correct_responses).
       """
       correct_count = 0
       missed_count = 0
       incorrect_count = 0

       for i, event_data in self.correct_responses.items():
           # Extract expected keys
           exp_pos = event_data["expected_position"]
           exp_num = event_data["expected_number"]

           pl_pos, pl_num = self.player_responses.get(i, (None, None))

           pos_result = self.classify_key(exp_pos, pl_pos)
           num_result = self.classify_key(exp_num, pl_num)


           # Assign correctness scores: correct = 1, incorrect = 0, missed = 0
           pos_score = 1 if pos_result == 'correct' else 0
           num_score = 1 if num_result == 'correct' else 0
           total_score = pos_score + num_score

           correct_count = total_score

           for result in [pos_result, num_result]:
               if result == 'missed':
                   missed_count += 1
               elif result == 'incorrect':
                   incorrect_count += 1
       return {'correct': correct_count, 'missed_count': missed_count, 'incorrect': incorrect_count}























