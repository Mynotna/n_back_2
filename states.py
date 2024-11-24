import pygame
from settings import WIDTH, HEIGHT


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
        pass

    def render(self):
        screen.fill((69, 69, 69))
        pass

class IntroState(State):
    def __init__(self, game):
        super().__init__(game)

        #Access resources
        self.bg_image = self.game.resources.images["intro_bg"]
        self.font = self.game.resources.fonts["main"]

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.current_state = self.game.states["GetReadyState"]

    def update(self, dt):
        pass

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))
        text_surface = self.font.render("Welcome to the game, Dwindle", True, (211, 99, 35))
        text_surface_rect = text_surface.get_rect(center= (WIDTH / 2, HEIGHT / 2))
        screen.blit(text_surface, text_surface_rect)

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
        font = self.game.resources.fonts["menu"]
        text_surface = font.render("Get Ready, Dwindle", True, (179, 122, 180))
        text_rect = text_surface.get_rect(center= (WIDTH / 2, HEIGHT / 2))
        screen.blit(text_surface, text_rect)


class GamePlayState(State):

    def __init__(self):
        self.game_box = self.game.resources.images["geme_box"]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    print("Store 'position' click press in list?")
                elif event.key == pygame.K_j:
                    print("Store 'number' press in list")

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((5, 13, 55))
        game_box_surf = self.game_box
        game_box_rect = game_box_surf.get_rect(center= (WIDTH / 2, HEIGHT / 2))
        screen.blit(game_box_surf, game_box_rect)



class FinishState(State):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print("play again")
                else:
                    self.running = False
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((55, 233, 21))
        font = self.game.resources.fonts["menu"]
        text_surf = font.render("All over, Dwindle", True, (101, 78, 134))
        text_surf_rect = text_surf.get_rect(center= (WIDTH /2, HEIGHT / 2))
        screen.blit(text_surf, text_surf_rect)






