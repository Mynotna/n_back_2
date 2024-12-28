import pygame

def handle_text_input(events, current_text):
    """Called from the IntroState in game_manager"""
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Return the text and flip the flag indicating completion
                return current_text, True
            elif event.key == pygame.K_BACKSPACE:
                current_text = current_text[:-1]
            else:
                char = event.unicode
                if char.isprintable():
                    current_text += char
    return current_text, False