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
            "one": pygame.mixer.Sound("assets/audio/one.wav"),
            "two": pygame.mixer.Sound("assets/audio/two.wav"),
            "three": pygame.mixer.Sound("assets/audio/three.wav"),
            "four": pygame.mixer.Sound("assets/audio/four.wav"),
            "five": pygame.mixer.Sound("assets/audio/five.wav"),
            "six": pygame.mixer.Sound("assets/audio/six.wav"),
            "seven": pygame.mixer.Sound("assets/audio/seven.wav"),
            "eight": pygame.mixer.Sound("assets/audio/eight.wav"),
            "nine": pygame.mixer.Sound("assets/audio/nine.wav")
        }

        self.fonts = {
            "main": pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 32),
            "menu": pygame.font.Font("assets/fonts/Poppins-ExtraBold.ttf", 12)
        }