import random

import pygame
import pygame.time

from settings import WIDTH, HEIGHT
from random import shuffle, choice, randint


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

    def __init__(self, game):
        super().__init__(game)
        self.game_box = self.game.resources.images["game_box"]
        self.game_box_rect = self.game_box.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.font = self.game.resources.fonts["main"]

        # Game logic variables
        self.num_count = 0
        self.num_per_round = 0
        self.current_number = None
        self.current_coord = None
        self.coordinates_list = []
        self.coord_index = 0
        self.display_number_time = 1000
        self.last_number_time = pygame.time.get_ticks()

        #Initialize shuffled coordinates
        self.shuffle_coordinates()


    def shuffle_coordinates(self):
        self.coordinates_list = list(self.game.resources.tablet_coords.values())
        random.shuffle(self.coordinates_list)
        self.coord_index = 0 # Resets index to start from beginning


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    #Add logic to update lists which record the player's inputs
                    pass
                elif event.key == pygame.K_j:
                    #Add logic to update lists which record the player's inputs
                    pass

    def update(self, dt):
        """Update the game logic"""

        current_time = pygame.time.get_ticks()

        if self.num_count >= self.num_per_round and self.current_number is None:
            #All coordinates have used; transition to another state
            self.game.current_state = self.game.states["FinishState"]
        else:
            if self.current_number in None:
                if current_time - self.last_number_time >= self.display_number_time:
                    # Get the next coordinate from the shuffled list
                    if self.coord_index < len(self.coordinates_list):
                        self.current_coord = self.coordinates_list[self.coord_index]
                        self.coord_index += 1
                    else:
                        # Reset if necessary (e.g., for a new round)
                        self.shuffle_coordinates()
                        self.current_coord = self.coordinates_list[self.coord_index]
                        self.coord_index += 1

                    # Generate random number
                    self.current_number = random.randint(1, 9)
                    self.num_count += 1
                    self.last_number_time = current_time

    def render(self, screen):
        screen.fill((5, 13, 55))
        screen.blit(self.game_box, self.game_box_rect)

        # Render the current number at the selected coordinate
        if self.current_number is not None and self.current_coord is not None:
            rand_num_surf = self.font.render(str(self.current_number), True, (233, 144, 89))
            rand_num_surf_rect = rand_num_surf.get_rect(center=self.current_coord)
            screen.blit(rand_num_surf, rand_num_surf_rect)


class FinishState(State):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.game.current_state = self.game.states["IntroState"]
                elif event.key == pygame.K_q:
                    self.game.running = False


    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((55, 233, 21))
        font = self.game.resources.fonts["menu"]
        text_surf = font.render("All over, Dwindle", True, (101, 78, 134))
        text_surf_rect = text_surf.get_rect(center= (WIDTH /2, HEIGHT / 2))
        screen.blit(text_surf, text_surf_rect)






