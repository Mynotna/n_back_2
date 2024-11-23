import pygame


class State:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game.running = False

    def update(self, dt):
        raise NotImplementedError("handle_events() must be overridden in the subclass.")

    def render(self):
        raise NotImplementedError("handle_events() must be overridden in the subclass.")

class IntroState(State):
    def __init__(self, game):
        super().__init__(game)
    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.current_state = self.game.game.states["GetReadyState"]

    def update(self, dt):
        pass

    def render(self, screen):
        pass

class GetReadyState(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = pygame.time.get_ticks()
        self.delay = 2000

    def handle_events(self, events):
        pass

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.delay:
            # Transition to0 Gameplay state
            self.game.current_state = self.game.states["GamePlayState"]
        pass

    def render(self, screen):
        screen.fill((0, 90, 13))
        print("Get Ready, Spume")

class GamePlayState(State):
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

class FinishState(State):
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass





