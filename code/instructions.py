import pygame

def show_training_instructions(screen, font):
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen or set it to a background

        # Display instructions
        instructions_text = [
            "Welcome to Whack-a-Pirate!",
            "Instructions:",
            "1. Pirates will appear randomly - hit them as fast as you can.",
            "2. Avoid hitting the bombs.",
            "Press any key to continue..."
        ]
        y_offset = 100
        for line in instructions_text:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (100, y_offset))
            y_offset += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Indicates the game should exit
            elif event.type == pygame.KEYDOWN:
                running = False
                return True  # Indicates the user is ready to proceed
            
        pygame.display.flip()


def show_game_instructions(screen, font):
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear the screen or set it to a background

        # Display instructions
        instructions_text = [
            "Blah"
        ]
        y_offset = 100
        for line in instructions_text:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (100, y_offset))
            y_offset += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Indicates the game should exit
            elif event.type == pygame.KEYDOWN:
                running = False
                return True  # Indicates the user is ready to proceed
            
        pygame.display.flip()