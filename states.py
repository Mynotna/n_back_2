import logging
import random
import pygame
import pygame.time
import pygame.mixer

from data_manager import DataManager
from random_gen import RandomGenerator
from score_manager import ScoreManager
from datetime import datetime

from resources import ResourceManager

from settings import WIDTH, HEIGHT, COLOR

import logging

# configure logger
logging.basicConfig(level= logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



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
        self.instruct_btn_rect = self.instruct_btn.get_rect(center=(ResourceManager.get_tablet_coords()[1]))

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
        self.delay = 3000

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
    """Numbers are placed using coordinates
    Instructions are blitted to the screen as png files
    """
    def __init__(self, game):
        super().__init__(game)
        self.game_box = self.game.resources.images["game_box"]
        self.game_box_rect = self.game_box.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.font = self.game.resources.fonts["main"]

        # Initialise RandomGenerator and get n_back lists for displaying numbers in positions, and correct_responses
        # to call score_manager
        self.n_back_value = 2
        self.random_gen = RandomGenerator(n=self.n_back_value)
        self.generate_new_sequences()
        # self.reset()



        # Initialise player response dictionary
        self.player_responses = {}

        # Initialise instances DataManager and ScoreManager
        self.data_manager = DataManager()
        self.score_manager = ScoreManager(self.player_responses, self.correct_responses)

        # Start new session
        self.data_manager.start_new_session()

        # Game and session tracking
        self.num_per_game = len(self.correct_responses)
        self.games_per_session = 10
        self.game_count = 0

        # Timing and display
        self.display_number_time = 200
        self.last_number_time = pygame.time.get_ticks()
        self.num_count = 0

        # Current event's data
        self.current_number = None
        self.current_coord = None

        #Get audio files
        self.audio_files = self.game.resources.sounds

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

        # Start a new session
        self.data_manager.start_new_session()

    def generate_new_sequences(self):
        """Generate new sequences of numbers and coordinates per game"""
        self.n_back_numbers, self.n_back_coords = self.random_gen.random_list_generator()
        self.correct_responses = self.random_gen.generate_correct_responses(
            self.n_back_numbers,
            self.n_back_coords,
            self.n_back_value
        )
    def reset(self):
        """Reset the game logic for a new round."""
        # Score counting variables
        self.correct_count = 0
        self.missed_count = 0

        self.num_count = 0
        self.num_per_game = 10
        self.games_per_session = 10

        self.current_number = None
        self.current_coord = None

        self.display_number_time = 200
        self.last_number_time = pygame.time.get_ticks()

        self.player_responses.clear()

        # Create new coordinate and number lists
        self.generate_new_sequences()

        # Trigger countdown
        self.count_down()

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_g, pygame.K_j):
                    # Indentify the current event index (last one displayed)
                    current_event_index = self.num_count -1
                    if current_event_index in self.player_responses:
                        current_position_key, current_number_key = self.player_responses[current_event_index]

                        # Only record the first key press from player
                        if current_position_key is None and current_number_key is None:
                            if event.key == pygame.K_g:
                                # g pressed for position
                                self.player_responses[current_event_index] = ('g', None)
                                logger.info(f"g pressed: {current_event_index}")

                            if event.key == pygame.K_j:
                                # j pressed for number
                                self.player_responses[current_event_index] = (None, 'j')
                                logger.info(f"j pressed: {current_event_index}")
                        logger.info(f"player_responses: {self.player_responses}")


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

        # Display new number if none currently displayed using correct_responses dict from RandomGenerator
        if self.current_number is None:
            # Check if it's time to display new number
            if current_time - self.last_number_time >= self.display_number_time:
                if self.num_count < len(self.n_back_numbers):
                    event_data = self.correct_responses[self.num_count]
                    self.current_number = event_data["number"]
                    self.current_coord = event_data["coord"]
                    self.last_number_time = current_time

                    #Initialise player_responses for this event index
                    self.player_responses[self.num_count] = (None, None)

                    # Increment self.num_count since new event just started
                    self.num_count += 1

                    # Play audio files
                    if self.current_number in self.audio_files:
                        sound = self.audio_files[self.current_number]
                        if sound:
                            sound.play()
                        else:
                            logging.error(f"No audio files to play")
                else:
                    # No more coords or numbers. Bring game to an end
                    self.game_count += 1
                    logger.info(f"game_count: {self.game_count}")
                    self.end_game()

        else:
            # Clear the number after display time expires
            if current_time - self.last_number_time >= self.display_number_time:
                self.current_number = None
                self. current_coord = None


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
            return # Skips rendering game_box during countdown

        # Render the current number at the selected coordinate
        if self.current_number is not None and self.current_coord is not None:
            rand_num_surf = self.font.render(str(self.current_number), True, (233, 144, 89))
            rand_num_surf_rect = rand_num_surf.get_rect(center=self.current_coord)
            screen.blit(rand_num_surf, rand_num_surf_rect)


    def end_game(self):
        """calculate results and transition to GameResultState"""
        results = self.score_manager.evaluate_score()

        # save each event to the database now results are known
        for i, event_data in self.correct_responses.items():
            # event_data contains {"number", "coord", "expected_position_key", "expected_number_key"}
            player_pos, player_num = self.player_responses.get(i, (None, None))

            # Classify correctness for number and position
            pos_result = self.score_manager.classify_key(event_data["expected_position_key"], player_pos)
            num_result = self.score_manager.classify_key(event_data["expected_number_key"], player_num)

            self.data_manager.save_game_event(
                session_id=self.data_manager.session_id,
                game_id= self.game_count,
                event_index= i,
                n_back_value= self.random_gen.n,
                actual_number= event_data["number"],
                player_number_response= 1 if player_num == "j" else None,
                number_response_status= num_result,
                actual_position= event_data["coord"],
                player_position_response= event_data["coord"] if player_pos == "g" else None,
                position_response_status= pos_result
            )

            # Transition to the result state
        session_results = {
            "correct": results["correct"],
            "missed": results["missed_count"]
        }
        if self.game_count >= self.games_per_session:
            #Aggregate results
            aggregated_results = {"correct": results["correct"], "missed": results["missed_count"]}
            session_rank = 1
            self.game.transition_to_finish_state(session_results)
        else:
            self.game.transition_to_game_result_state(session_results)


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
                    self.game.current_state = self.game.states["GamePlayState"]
                elif self.button_rects["exit"].collidepoint(event.pos):
                    # End the session
                    self.game.transition_to_finish_state()


    def render(self, screen):
        screen.fill((0, 144, 233))
        font = self.game.resources.fonts["btn_1"]
        # Display session results
        results_text = f"Results: {self.session_results["correct"]} correct, {self.session_results["missed"]}"
        results_surf = font.render(results_text, True, (211, 211, 144))
        results_rect = results_surf.get_rect(center= (WIDTH // 2, HEIGHT //3))
        screen.blit(results_surf, results_rect)

        # Draw next_game and exit buttons
        pygame.draw.rect(screen, (111, 211, 211), self.button_rects["next_game"])
        pygame.draw.rect(screen, (111, 212, 211), self.button_rects["exit"])

        # Render button text
        next_game_text = font.render("Next game?", True, (89, 89, 21))
        next_game_rect = next_game_text.get_rect(center= self.button_rects["next_game"].center)
        screen.blit(next_game_text, next_game_rect)

        exit_text = font.render("Exit?", True, (89, 89, 21))
        exit_text_rect = exit_text.get_rect(center= self.button_rects["exit"].center)
        screen.blit(exit_text, exit_text_rect)


class FinishState(State):
    def __init__(self, game, aggregated_results, session_rank):
        super().__init__(game)
        self.aggregated_results = aggregated_results
        self.session_rank = session_rank
        self.button_rects = self.create_buttons()


    def create_buttons(self):
        """Create Play again and Exit buttons"""
        restart_button = pygame.Rect((WIDTH //2 - 100, HEIGHT //2 + 50, 200, 50))
        exit_button = pygame.Rect((WIDTH //2 - 100, HEIGHT //2 + 120, 200, 50))
        return {"restart": restart_button, "exit": exit_button}

        # Store results
        self.session_results = None
        self.aggregated_results = None


    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rects["restart"].collidepoint(event.pos):
                    # Reset entire session
                    self.game.reset_session()
                    self.game.current_state = self.game.states["IntroState"]
                elif self.button_rects["exit"].collidepoint(event.pos):
                    self.game.running = False


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












