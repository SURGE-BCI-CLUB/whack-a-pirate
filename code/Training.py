import pygame
import random
import sys
import numpy as np
#import psychopy
from math import sin, cos, pi
from Button import *
from Pirate import *


class Training:

    def start_training(nickname ,game_mode, pirate_sprites, screen, start_button):
            # Get a list of all pirates and shuffle it
        
        all_pirates = list(pirate_sprites.sprites())
        random.shuffle(all_pirates)

        if game_mode == "Flicker-oddball":
            print('hello')

            training = True
            clock = pygame.time.Clock()


            for target_pirate in all_pirates:
                training = True

                while training:
                    # Display silhouette of the "target" pirate for 2 seconds
                    start_time = pygame.time.get_ticks()
                    while pygame.time.get_ticks() - start_time < 2000:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                training = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                                    training = False
                                    pygame.quit()
                                    sys.exit()
                                    
                        if not training:
                            break
                        screen.fill((0, 0, 0))
                        target_pirate.draw_silhouette(screen)
                        pygame.display.flip()
                        clock.tick(60)

                    # Flicker each pirate in the shuffled list for 2 seconds
                    for pirate in all_pirates:
                        # Reset the start time for the flickering phase
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 2000:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    training = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    if start_button.is_clicked(pos):
                                        training = False
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                                        training = False
                                        pygame.quit()
                                        sys.exit()

                            # Update pirate visibility
                            current_time = pygame.time.get_ticks()
                            phase = ((current_time - start_time) % (pirate.duration * 1000)) / (pirate.duration * 1000)
                            pirate.visible = np.sin(2 * np.pi * phase) > 0

                            # Clear the screen
                            screen.fill((0, 0, 0))

                            # Draw current pirate
                            pirate.draw(screen)

                            # Update the display
                            pygame.display.flip()

                            # Set the frame rate
                            clock.tick(60)

                        pirate.visible = False
                    training = False
                        
        elif game_mode == "Flicker+odd":
            training = True
            clock = pygame.time.Clock()

            # Get a list of all pirates
            all_pirates = list(pirate_sprites.sprites())
            pirate_counts = {pirate: 0 for pirate in all_pirates}

            # Start the flickering phase
            start_time = pygame.time.get_ticks()

            # Initialize current pirate and its display time
            current_pirate = random.choice(all_pirates)
            pirate_counts[current_pirate] += 1
            current_pirate.visible = True  # Make the current pirate visible
            pirate_display_time = pygame.time.get_ticks()

            while any(count < 6 for count in pirate_counts.values()):  # Until each pirate has been selected 6 times
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        training = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if start_button.is_clicked(pos):
                            training = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                            training = False
                            pygame.quit()
                            sys.exit()

                # Update pirate visibility
                current_time = pygame.time.get_ticks()
                for pirate in all_pirates:
                    if pirate != current_pirate:  # Skip the current pirate
                        phase = ((current_time - start_time) % (pirate.duration * 1000)) / (pirate.duration * 1000)
                        pirate.visible = np.sin(2 * np.pi * phase) > 0

                # Check if 2 seconds have passed since the current pirate was displayed
                if pygame.time.get_ticks() - pirate_display_time >= 500:  # 2 seconds
                    # Select a new pirate to display
                    current_pirate.visible = False  # Make the previous pirate invisible
                    available_pirates = [pirate for pirate, count in pirate_counts.items() if count < 6]
                    if available_pirates:
                        new_pirate = random.choice(available_pirates)
                        while new_pirate == current_pirate:
                            new_pirate = random.choice(available_pirates)
                        current_pirate = new_pirate
                        pirate_counts[current_pirate] += 1
                        current_pirate.visible = True  # Make the new pirate visible
                        pirate_display_time = pygame.time.get_ticks()

                # Clear the screen
                screen.fill((0, 0, 0))

                # Draw all pirates
                for pirate in all_pirates:
                    if pirate.visible:
                        pirate.draw_silhouette(screen)

                current_pirate.draw(screen)

                # Update the display
                pygame.display.flip()

                # Set the frame rate
                clock.tick(60)

            for pirate in all_pirates:
                pirate.visible = False
        else: 
            None

        # In your main function, call the home page function before the game loop
        # nickname, game_mode = home_page(screen, font)
        # if nickname and game_mode:
        #     # Start the training phase
        #     start_training(nickname, game_mode)
        #     game_loop(nickname, game_mode)

        # Wait for Start Game button to be clicked
        waiting = True
        while waiting:
            # Draw Start Game button
            start_button.draw(screen)

            # Update the display
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(pos):
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                        waiting = False
                        running = False