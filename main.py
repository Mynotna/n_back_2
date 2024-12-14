import pygame
import pygame.mixer
import sys
from states import State, IntroState, GamePlayState, GetReadyState, FinishState, GameResultState
from settings import WIDTH, HEIGHT
from resources import ResourceManager

pygame.mixer.init()
pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.resources = ResourceManager()
        self.running = True
        self.clock = pygame.time.Clock()

        # Initialize states and results tracking
        self.states = {}
        self.current_state = None
        self.aggregated_results = {"correct": 0, "missed": 0} # Track overall results
        self.load_states()

    def load_states(self):
        self.states["IntroState"] = IntroState(self)
        self.states["GetReadyState"] = GetReadyState(self)
        self.states["GamePlayState"] = GamePlayState(self)

        self.current_state = self.states["IntroState"]


    def reset_session(self):
        """ Reset the game session to start over"""
        self.aggregated_results = {"correct": 0, "missed": 0}

        # Reset all states
        self.load_states()

        # Transition back to old state
        self.current_state = self.states["IntroState"]


    def transition_to_game_result_state(self, session_results):
        """
                Transition to GameResultState after a game session ends.
                Updates aggregated results and creates a new GameResultState instance.
                """
        self.aggregated_results["correct"] += session_results["correct"]
        self.aggregated_results["missed"] += session_results["missed"]

        # Create a new GameResultState and transition it
        self.states["GameResultState"] = GameResultState(self, session_results)
        self.current_state = self.states["GameResultState"]


    def transition_to_finish_state(self):
        """Transition to FinishState where all results are displayed
        Included aggregated results"""

        session_rank = f"Rank #{len(self.aggregated_results)}"
        # Create a new Finish state and transition to it
        self.states["FinishState"] = FinishState(self, self.aggregated_results, session_rank)
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

if __name__ == "__main__":
    game = Game()
    game.run()
