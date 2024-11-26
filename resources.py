import pygame


class ResourceManager:

    def __init__(self):
        self.images = {
            "intro_bg": pygame.image.load("assets/graphics/Backgrounds/trans_bg.png").convert_alpha(),
            "game_box": pygame.image.load("assets/graphics/Backgrounds/game_grid.png").convert_alpha(),
            "instruct_1": pygame.image.load("assets/graphics/instruct_imgs/1_instr.png").convert_alpha(),
            "instruct_2": pygame.image.load("assets/graphics/instruct_imgs/2_instr.png").convert_alpha(),
            "instruct_3": pygame.image.load("assets/graphics/instruct_imgs/3_instr.png").convert_alpha(),
            "instruct_4": pygame.image.load("assets/graphics/instruct_imgs/4_instr.png").convert_alpha(),
            "instruct_5": pygame.image.load("assets/graphics/instruct_imgs/5_instr.png").convert_alpha(),
            "instruct_6": pygame.image.load("assets/graphics/instruct_imgs/6_instr.png").convert_alpha(),
            "instruct_7": pygame.image.load("assets/graphics/instruct_imgs/7_instr.png").convert_alpha(),
            "instruct_8": pygame.image.load("assets/graphics/instruct_imgs/8_instr.png").convert_alpha(),
            "instruct_9": pygame.image.load("assets/graphics/instruct_imgs/9_instr.png").convert_alpha()
        }
        self.sounds = {
            1: pygame.mixer.Sound("assets/audio/one.wav"),
            2: pygame.mixer.Sound("assets/audio/two.wav"),
            3: pygame.mixer.Sound("assets/audio/three.wav"),
            4: pygame.mixer.Sound("assets/audio/four.wav"),
            5: pygame.mixer.Sound("assets/audio/five.wav"),
            6: pygame.mixer.Sound("assets/audio/six.wav"),
            7: pygame.mixer.Sound("assets/audio/seven.wav"),
            8: pygame.mixer.Sound("assets/audio/eight.wav"),
            9: pygame.mixer.Sound("assets/audio/nine.wav")
        }

        self.fonts = {
            "main": pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 89),
            "menu": pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 34),
            "btn_1": pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 21)
        }

        self.tablet_coords = {
            1: (150, 155),
            2: (400, 155),
            3: (650, 155),
            4: (150, 405),
            5: (650, 405),
            6: (150, 655),
            7: (400, 655),
            8: (650, 655),
        }

        self.instruction_coords = {
            1: (150, 155),
            2: (400, 155),
            3: (650, 155),
            4: (150, 405),
            5: (650, 405),
            6: (150, 680),
            7: (400, 680),
            8: (650, 655),
            9: (400, 400)
        }
