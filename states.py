import random
import pygame
import pygame.time
import pygame.mixer

from data_manager import DataManager
from score_manager import ScoreManager
from datetime import datetime


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

        self.ct_dwn_btn_3 = self.game.resources.images["ct_dwn_3"]
        self.ct_dwn_btn_3_rect = self.ct_dwn_btn_3.get_rect(center=(WIDTH /2, HEIGHT /2))

        self.ct_dwn_btn_2 = self.game.resources.images["ct_dwn_2"]
        self.ct_dwn_btn_2_rect = self.ct_dwn_btn_2 .get_rect(center=(WIDTH /2, HEIGHT /2))

        self.ct_dwn_btn_1 = self.game.resources.images["ct_dwn_1"]
        self.ct_dwn_btn_1_rect = self.ct_dwn_btn_1.get_rect(center=(WIDTH /2, HEIGHT /2))

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

        # Get countdown images and put in list
        self.count_down_images = [
            self.game.resources.images["ct_dwn_3"],
            self.game.resources.images["ct_dwn_2"],
            self.game.resources.images["ct_dwn_1"]
        ]
        # Set countdown variables
        self.is_counting_down = False
        self.current_countdown_index = 0
        self.count_down_start_time = 0

        #Initialise DataManager and ScoreManager
        self.data_manager = DataManager()
        self.score_manager = ScoreManager(n_back=2)

        # Start a new session
        self.data_manager.start_new_session()

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

        self.display_number_time = 1500
        self.last_number_time = pygame.time.get_ticks()

        self.shuffle_coordinates()

        # Trigger countdown
        self.count_down()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    #Player indicates position match
                    input_time = pygame.time.get_ticks()
                    self.score_manager.add_player_input(input_time, 'position')
                    is_correct = int(self.score_manager.check_position_match())
                    missed = 0
                    self.data_manager.save_response(
                        datetime.now().isoformat(), 'position', is_correct, missed
                    )
                elif event.key == pygame.K_j:
                    # Player indicates position match
                    input_time = pygame.time.get_ticks()
                    self.score_manager.add_player_input(input_time, 'number')
                    is_correct = int(self.score_manager.check_number_match())
                    missed = 0
                    self.data_manager.save_response(
                        datetime.now().isoformat(), 'number', is_correct, missed
                    )

    def update(self, dt):
        """Update the game logic"""

        current_time = pygame.time.get_ticks()

        if self.is_counting_down:
            if current_time - self.count_down_start_time >= 1000:
                self.current_countdown_index += 1
                self.count_down_start_time = current_time

                if self.current_countdown_index >= len(self.count_down_images):
                    self.is_counting_down = False
                    self.current_countdown_index = 0
            return

        # Handle other game updates
        super().update(dt)

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

                # Append generated data to ScoreManager
                self.score_manager.add_generated_data(self.current_number, self.current_coord)

                # Save generated data to database
                timestamp = datetime.now().isoformat()
                self.data_manager.save_generated_data(timestamp, self.current_number, self.current_coord)

                # Play audio files matching the numbers
                if self.current_number in self.audio_files:
                    self.audio_files[self.current_number].play()

        else:
            #Clear the current number and coordinate
            if current_time - self.last_number_time >= self.display_number_time:
                self.current_number = None
                self.current_coord = None

    def check_missed_response(self):
        missed_number, missed_position = self.score_manager.check_missed_responses()
        timestamp = datetime.now().isoformat()

        if missed_number:
            self.data_manager.save_response(timestamp, 'number', is_correct=0, missed=1)

        if missed_position:
            self.data_manager.save_response(timestamp, 'position', is_correct=0, missed=1)

    def count_down(self):
        self.is_counting_down = True
        self.current_countdown_index = 0
        self.count_down_start_time = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((5, 13, 55))
        # Render game_box
        screen.blit(self.game_box, self.game_box_rect)

        if self.is_counting_down:
            count_down_image = self.count_down_images[self.current_countdown_index]
            count_down_image_rect = count_down_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(count_down_image, count_down_image_rect)
            print("countdown tabs stuff is happening")
            return # Skips rendering game_box during countdown

        # Render the current number at the selected coordinate
        if self.current_number is not None and self.current_coord is not None:
            rand_num_surf = self.font.render(str(self.current_number), True, (233, 144, 89))
            rand_num_surf_rect = rand_num_surf.get_rect(center=self.current_coord)
            screen.blit(rand_num_surf, rand_num_surf_rect)

    def __del__(self):
        if hasattr(self, 'data_manager') and self.data_manager:
            self.data_manager.close()

class GameResultState(State):
    def __init__(self, game, session_results):
        super().__init__(game)
        self.session_results = session_results  # results of the current session
        self.button_rects = self.create_buttons()

    def create_buttons(self):
        """Create the buttons for Next Game and exit"""
        next_game_button = pygame.Rect(WIDTH //2 -100, HEIGHT // 2 + 50, 200, 50)
        exit_button = pygame.Rect(WIDTH //2 -100, HEIGHT //2 + 120, 200, 50)
        return {"next_game": next_game_button, "exit": exit_button}


    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rects["next_game"].collidepoint(event.pos):
                    # Start the next game
                    self.game.states["GamePlayState"].reset()
                    self.current_state = self.game.states["GamePlayState"]
                elif self.button_rects["exit"].collidepoint(event.pos):
                    # End the session
                    self.game.current_state = self.game.states["FinishState"]


    def render(self, screen):
        screen.fill((0, 144, 233))
        font = self.game.resources.fonts["menu"]
        # Display session results
        results_text = f"Results: {self.session_results["correct"]} correct, {self.session_results["missed"]}"
        results_surf = font.render(results_text, True, (211, 211, 144))
        results_rect = results_surf.get_rect(center= (WIDTH // 2, HEIGHT //3))
        screen.blit(results_surf, results_rect)

        # Draw next_game and exit buttons
        pygame.draw.rect(screen, (111, 211, 211), self.button_rects["next_game"])
        pygame.draw.rect(screen, (111, 212, 211), self.button_rects["exit"])

        # Render button text
        next_game_text = font.render("Next game?", True, (233, 89, 21))
        next_game_rect = next_game_text.get_rect(center= self.button_rects["next_game"])
        screen.blit(next_game_text, next_game_rect)

        exit_text = font.render("Exit?", True, (89, 211, 239))
        exit_text_rect = exit_text.get.rect(center= self.button_rects["exit"])
        screen.blit(exit_text, exit_text_rect)


class FinishState(State):
    def __init__(self, game, aggregated_results, session_rank):
        super().__init__(game)
        self.aggregated_results = aggregated_results
        self.session_rank = session_rank
        self.button_rects = self.create_buttons()


    def create_buttons(self):
        """Create Play again and Exit buttons"""
        restart_button = pygame.draw.rect((WIDTH //2 - 100, HEIGHT //2 + 50, 200, 50))
        exit_button = pygame.draw.rect((WIDTH //2 - 100, HEIGHT //2 + 120, 200, 50))
        return {"restart": restart_button, "exit": exit_button}

        # Store results
        self.session_results = None
        self.aggregated_results = None


    # def reset(self, session_results, aggregated_results):
    #     """Reinitialize the state with results"""
    #     self.start_time = pygame.time.get_ticks()
    #     self.show_play_again_text = False
    #     self.session_results = session_results
    #     self.aggregated_results = aggregated_results
    #     print("FinishState reset with the new results.")


    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.button_rects["restart"].collidepoint():
                    # Reset entire session
                    self.game.reset_session()
                    self.game.current_state = self.game.states["introState"]
                elif self.button_rects["exit"].collidepoint():
                    self.game.running = False


    # def update(self, dt):
    #     current_time = pygame.time.get_ticks()
    #     elapsed_time = current_time - self.start_time
    #     if elapsed_time >= self.play_again_delay:
    #         self.show_play_again_text = True


    def render(self, screen):
        screen.fill((55, 233, 21))
        font = self.game.resources.fonts["menu"]

        # Display aggregate results
        agg_text = f"Total: {self.aggregated_results["correct"]} correct, {self.aggregated_results["missed"]} missed"
        agg_surf = font.render(agg_text, True, (199, 0, 211))
        agg_rect = agg_surf.get_rect(center= (WIDTH // 2, HEIGHT // 3))
        screen.blit(agg_surf, agg_rect)

        # Display rank
        rank_text = f"Rank: {self.session_rank}"
        rank_surf = font.render(rank_text, True, (11, 89, 11))
        rank_rect = rank_surf.get_rect(center= (WIDTH // 2, HEIGHT // 2))
        screen.blit(rank_surf, rank_rect)

        # Draw buttons
        restart_text = font.render("Restart?", True, (141, 21, 42))
        restart_rect = restart_text.get_rect(center= self.button_rects["restart"].center)
        screen.blit(restart_text, restart_rect)

        exit_text = font.render("Exit?", True, (141, 21, 42))
        exit_rect = exit_text.get_rect(center= self.button_rects["exit"].center)
        screen.blit(exit_text, exit_rect)












