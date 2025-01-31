import json
import pandas as pd


class ScoreManager:
    def __init__(self, player_responses, correct_responses, n):

        """The ScoreManager receives a dictionary (self.player_responses) from GamePlayState,
        and a correct_responses dictionary from RandomGenerator class and compares the two. It also gives numerical
        values to responses and aggregates them across the 10 games of a round
        They both should have
        exactly the same format for comparison and scoring, i.e.
        {
        0: (None, None),
        1: (j, None),
        2: (None, g)
        ditto
        }
        """
        self.n = n

        # Initialise player_responses dictionary from GamePlayState class
        self.player_responses = player_responses
        # Initialise correct_responses dictionary from Random_gen class
        self.correct_responses = correct_responses

        # Initialise the aggregate scores dictionary to accumulate scores over the 10 games of a round
        self.aggregate_results = {"correct": 0, "incorrect": 0, "missed": 0}


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

    def aggregate_scores(self, game_results):
        self.aggregate_results["correct"] += game_results["correct"]
        self.aggregate_results["incorrect"] += game_results["incorrect"]
        self.aggregate_results["missed"] += game_results["missed"]
        return self.aggregate_results

    def evaluate_game_score(self):
        """This evaluates the player's score by comparing two dictionaries, one from the GamePlayState
        (player_responses), the other from RandomGenerator (correct_responses).
        Also creates a dictionary of correct/incorrect status values to be added to game_events table.
        """
        data = []

        for i, event_data in self.correct_responses.items():
            # Extract expected keys
            exp_pos = event_data["expected_position_key"]
            exp_num = event_data["expected_number_key"]
            # Get player's responses
            pl_pos, pl_num = self.player_responses.get(i, (None, None))

            # Classify responses (position and number)
            pos_result = self.classify_key(exp_pos, pl_pos)
            num_result = self.classify_key(exp_num, pl_num)

            data.append({
                "index": i,
                "expected_position": exp_pos,
                "expected_number": exp_num,
                "player_position": pl_pos,
                "player_number": pl_num,
                "position_result": pos_result,
                "number_result": num_result
            })

            #  Create dataframe
            df = pd.DataFrame(data)

            # Apply scoring logic
            df["pos_score"] = df["position_result"].apply(lambda x: 1 if x == "correct" else 0)
            df["num_score"] = df["number_result"].apply(lambda x: 1 if x == "correct" else 0)

            #Calculate total score for position and number
            df["total_score"] = df["pos_score"] + df["num_score"]

            #Penalise incorrect key presses in first n items
            df.loc[df["index"] < self.n, "total_score"] += df["position_result"].isin(["incorrect", "missed"]).astype(int) * -1
            df.loc[df["index"] < self.n, "total_score"] += df["number_result"].isin(["incorrect", "missed"]).astype(int) * -1

            #Count missed and incorrect responses
            missed_count = df[["position_result", "number_result"]].isin(["missed"]).sum().sum()
            incorrect_count = df[["position_result", "number_result"]].isin(["incorrect"]).sum().sum()

            correct_count = df["total_score"].sum()

            #Prepare game results for return
            game_results = {"correct": correct_count, "incorrect": incorrect_count, "missed": missed_count}

            #Aggregate scores across games for a round
            aggregate_score = self.aggregate_scores(game_results)

            print(f"Game results: {game_results}")
            print(f"Event results:\n{df}")
            print(f"Aggregate scores: {aggregate_score}")

        return game_results, df


    def orig_evaluate_game_score(self):
        """This evaluates the player's score by comparing two dictionaries, one from the GamePlayState
        (player_responses), the other from RandomGenerator (correct_responses).
        Also creates a dictionary of correct/incorrect status values to be added to game_events table.
        """
        correct_count = 0
        missed_count = 0
        incorrect_count = 0
        penalty = -1

        # Dictionary to store correct/incorrect values to pass to game_events table via end_game method in GamePlayState
        event_results = {}

        for i, event_data in self.correct_responses.items():
            # Extract expected keys
            exp_pos = event_data["expected_position_key"]
            exp_num = event_data["expected_number_key"]

            pl_pos, pl_num = self.player_responses.get(i, (None, None))

            # Classify responses (position and number)
            pos_result = self.classify_key(exp_pos, pl_pos)
            num_result = self.classify_key(exp_num, pl_num)

            # Store the results for each event to pass to game_events table
            event_results[i] = {"pos_result": pos_result, "num_result": num_result}

            # Assign correctness scores: correct = 1, incorrect = 0, missed = 0
            pos_score = 1 if pos_result == 'correct' else 0
            num_score = 1 if num_result == 'correct' else 0
            total_score = pos_score + num_score
            correct_count += total_score  # Accumulate correct scores

            if i < self.n:
                if pos_result == "incorrect" or num_result == "incorrect" or pos_result == "missed" or num_result == "missed":
                    total_score += penalty
                else:
                    correct_count += total_score

            # Count missed and incorrect responses for penalties
            for result in [pos_result, num_result]:
                if result == 'missed':
                    missed_count += 1
                elif result == 'incorrect':
                    incorrect_count += 1

        # Prepare game results for return
        game_results = {'correct': correct_count, 'incorrect': incorrect_count, 'missed': missed_count}

        # Aggregate the results
        self.aggregate_scores(game_results)
        print(f"Pos score: {pos_score}/nNum score: {num_score}/nGame results: {game_results}")
        print(f"Event_results: {event_results}")

        return event_results, game_results


if __name__ == "__main__":
    print("Hello")




















