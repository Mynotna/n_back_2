import pygame
import pygame.mixer
import sys
from states import State, IntroState, GamePlayState, GetReadyState, FinishState
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
        self.states = {}
        self.current_state = None
        self.load_states()

    def load_states(self):
        self.states["IntroState"] = IntroState(self)
        self.states["GetReadyState"] = GetReadyState(self)
        self.states["GamePlayState"] = GamePlayState(self)
        self.states["FinishState"] = FinishState(self)
        self.current_state = self.states["IntroState"]

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
