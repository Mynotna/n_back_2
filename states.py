import random

import pygame
import pygame.time
import pygame.mixer

from settings import WIDTH, HEIGHT, COLOR
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

    def render(self, screen):
        screen.fill((COLOR))

class IntroState(State):
    def __init__(self, game):
        super().__init__(game)

        #Access resources
        self.bg_image = self.game.resources.images["intro_bg"]
        self.font = self.game.resources.fonts["menu"]

        #Load images for Introstate, create rects
        self.instruct_scr = self.game.resources.images["instruct_scr"]
        self.instruct_scr_rect = self.instruct_scr.get_rect(center=(WIDTH /2, HEIGHT /2))

        self.enter_btn = self.game.resources.images["enter_btn"]
        self.enter_btn_rect = self.enter_btn.get_rect(center=(WIDTH /2, HEIGHT /2))

        self.instruct_btn = self.game.resources.images["instruct_btn"]
        self.instruct_btn_rect = self.instruct_btn.get_rect(center=(self.game.resources.tablet_coords[1]))

        self.ct_dwn_btn_1 = self.game.resources.images["ct_dwn_1"]
        self.ct_dwn_btn_1_rect = self.ct_dwn_btn_1.get_rect(center=(WIDTH /2, HEIGHT /2))

        self.ct_dwn_btn_2 = self.game.resources.images["ct_dwn_2"]
        self.ct_dwn_btn_2_rect = self.ct_dwn_btn_2 .get_rect(center=(WIDTH /2, HEIGHT /2))

        self.ct_dwn_btn_3 = self.game.resources.images["ct_dwn_3"]
        self.ct_dwn_btn_3_rect = self.ct_dwn_btn_3.get_rect(center=(WIDTH /2, HEIGHT /2))

        # Set start time and flag for blitting instructions and enter button
        self.start_time = pygame.time.get_ticks()
        self.show_start_time = False

        #Set flag for showing instruction screen
        self.show_instructions = False

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.instruct_btn_rect.collidepoint(event.pos):
                    self.show_instructions = True
                elif self.enter_btn_rect.collidepoint(event.pos):
                    self.game.current_state = self.game.states["GamePlayState"]

    def update(self, dt):
        # Calculate time since start
        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= 2000:
            self.show_start_time = True


    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # Blit enter button
        if self.show_start_time:
            screen.blit(self.enter_btn, self.enter_btn_rect)

            #Blit instruction button only if instructions screen not shown
            if not self.show_instructions:
                screen.blit(self.instruct_btn, self.instruct_btn_rect)

            #Blit instruction screen if "show_instruction' flag is True
            if self.show_instructions:
                screen.blit(self.instruct_scr, self.instruct_scr_rect)

class GetReadyState(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = pygame.time.get_ticks()
        self.delay = 5000

    def handle_events(self, events):
        pass

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.delay:
            # Transition to0 Gameplay state
            self.game.current_state = self.game.states["GamePlayState"]

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
        self.tablet_coords = game.resources.tablet_coords

        #Get audio files
        self.audio_files = game.resources.sounds

        # Convert coords to list
        self.tab_coords_list = list(self.tablet_coords.values())

        # Initialize shuffled coordinates
        self.shuffle_coordinates()

        # Initialise round variables
        self.num_of_rounds = 3
        self.current_round_num = 0

        # Call reset to initialize game logic variables
        self.reset()


    def shuffle_coordinates(self):
        random.shuffle(self.tab_coords_list)
        self.coord_index = 0 # Resets index to start from beginning

    def reset(self):
        """Reset the game logic for a new round."""
        self.num_count = 0
        self.num_per_round = 10

        self.current_number = None
        self.current_coord = None
        self.coord_index = 0

        self.display_number_time = 1000
        self.last_number_time = pygame.time.get_ticks()

        self.shuffle_coordinates()


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
            if self.current_round_num < self.num_of_rounds -1:
                # Move to the next round
                self.current_round_num += 1
                self.reset()
            else:
                # All rounds complete. Move to next round
                self.game.current_state = self.game.states["FinishState"]
            return

        if self.current_number is None:
            if current_time - self.last_number_time >= self.display_number_time:
                # Get the next coordinate from the shuffled list
                if self.coord_index < len(self.tab_coords_list):
                    self.current_coord = self.tab_coords_list[self.coord_index]
                    self.coord_index += 1
                else:
                    # Reset if necessary (e.g., for a new round)
                    self.shuffle_coordinates()
                    self.current_coord = self.tab_coords_list[self.coord_index]
                    self.coord_index += 1

                # Generate random number
                self.current_number = random.randint(1, 9)
                self.num_count += 1
                self.last_number_time = current_time

                # Play audio files matching the numbers
                if self.current_number in self.audio_files:
                    self.audio_files[self.current_number].play()

        else:
            #Clear the current number and coordinate
            if current_time - self.last_number_time >= self.display_number_time:
                self.current_number = None
                self.current_coord = None

    def render(self, screen):
        screen.fill((5, 13, 55))
        screen.blit(self.game_box, self.game_box_rect)

        # Render the current number at the selected coordinate
        if self.current_number is not None and self.current_coord is not None:
            rand_num_surf = self.font.render(str(self.current_number), True, (233, 144, 89))
            rand_num_surf_rect = rand_num_surf.get_rect(center=self.current_coord)
            screen.blit(rand_num_surf, rand_num_surf_rect)

class FinishState(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = pygame.time.get_ticks()
        self.play_again_delay = 2000 # Second delay
        self.show_play_again_text = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.game.states["GamePlayState"].reset()
                    self.game.current_state = self.game.states["IntroState"]
                elif event.key == pygame.K_n:
                    self.game.running = False


    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.play_again_delay:
            self.show_play_again_text = True

    def render(self, screen):
        screen.fill((55, 233, 21))
        font = self.game.resources.fonts["menu"]

        text_surf = font.render("All over, Dwindle", True, (101, 78, 134))
        text_surf_rect = text_surf.get_rect(center= (WIDTH /2, HEIGHT / 2))
        screen.blit(text_surf, text_surf_rect)

        if self.show_play_again_text:
            play_again_surf = font.render("Play again, Dwindle? Y or N?", True, (101, 78, 134))
            play_again_surf_rect = play_again_surf.get_rect(center= (WIDTH /2, 455))
            screen.blit(play_again_surf, play_again_surf_rect)






