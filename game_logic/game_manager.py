import pygame
import pygame.mixer
import sys
from game_logic.states import IntroState, GamePlayState, GetReadyState, FinishState, GameResultState
from config.config import WIDTH, HEIGHT
from game_logic.resource_manager import ResourceManager
from database.data_manager import DataManager

pygame.mixer.init()
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.resources = ResourceManager()
        self.running = True
        self.clock = pygame.time.Clock()

        # Initialise DataManager
        self.data_manager = DataManager()

        # Initialise player id
        self.player_id = ""

        # Initialize states and results tracking
        self.states = {}
        self.current_state = None
        self.round_results = {"correct": 0, "incorrect": 0, "missed": 0} # Track overall results
        self.load_states()

        #Initialise session object/id
        self.round_obj = None

    def set_session_obj(self, round_obj):
        self.round_obj = round_obj

    def load_states(self):
        self.states["IntroState"] = IntroState(self)
        self.states["GetReadyState"] = GetReadyState(self)
        self.states["GamePlayState"] = GamePlayState(self)

        self.current_state = self.states["IntroState"]


    def reset_session(self):
        """ Reset the game session to start over"""
        self.round_results = {"correct": 0, "incorrect": 0, "missed": 0}

        # Reset all states
        self.load_states()

        # Transition back to old state
        self.current_state = self.states["IntroState"]


    def transition_to_game_result_state(self, game_results, aggregate_results):
        """
                Transition to GameResultState after a game ends.
                Updates aggregated results and creates a new GameResultState instance.
                """
        self.round_results["correct"] += game_results["correct"]
        self.round_results["incorrect"] += game_results["incorrect"]
        self.round_results["missed"] += game_results["missed"]

        # Create a new GameResultState and transition to it
        self.states["GameResultState"] = GameResultState(self, game_results, aggregate_results)
        self.current_state = self.states["GameResultState"]


    def transition_to_finish_state(self, game_results, aggregate_results):
        """Transition to FinishState where all results are displayed
        Included aggregated results"""

        rank = f"Rank #{len(self.round_results)}"
        # Create a new Finish state and transition to it

        # Reset round results


        self.states["FinishState"] = FinishState(self, game_results, rank)
        self.current_state = self.states["FinishState"]


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # Delta time in seconds
            events = pygame.event.get()
            self.current_state.handle_events(events)
            self.current_state.update(dt)
            self.current_state.render(self.screen)
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__=="__main__":
    pygame.mixer.init()
    pygame.init()
    game = Game()
    game.run()