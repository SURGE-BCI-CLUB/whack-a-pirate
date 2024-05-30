import pygame
import random
import sys
import numpy as np
#import psychopy
from math import sin, cos, pi
from Button import *
from Pirate import *


class Game:
    
    @staticmethod
    def game_loop(nickname,game_mode, pirate_sprites, screen, font, start_button, running, current_pirate_index, score, clock):
        
        
        if game_mode == 'Flicker-oddball':

            start_time = pygame.time.get_ticks()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        pirate = pirate_sprites.sprites()[current_pirate_index]
                        if pirate.rect.collidepoint(pos) and pirate.visible:
                            score += 1
                            pirate.clicked = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                            running = False
                


                # Update pirate visibility
                current_time = pygame.time.get_ticks()
                if current_time - start_time < 2000:  # 2 seconds have passed
                    pirate = pirate_sprites.sprites()[current_pirate_index]
                    if not pirate.clicked:  # Only update visibility if pirate has not been clicked
                        phase = ((current_time - start_time) % (pirate.duration * 1000)) / (pirate.duration * 1000)
                        pirate.visible = np.sin(2 * np.pi * phase) > 0
                else:
                    pirate_sprites.sprites()[current_pirate_index].visible = False
                    pirate_sprites.sprites()[current_pirate_index].clicked = False  # Reset clicked status
                    current_pirate_index = (current_pirate_index + 1) % len(pirate_sprites.sprites())
                    start_time = current_time

                # Clear the screen
                screen.fill((0, 0, 0))

                # Draw current pirate
                pirate_sprites.sprites()[current_pirate_index].draw(screen)

                # Render the score
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                user_text = font.render(f"User: {nickname}", True, (255, 255, 255))
                screen.blit(user_text, (10, 40))
                screen.blit(score_text, (10, 10))

                # Update the display
                pygame.display.flip()

                # Set the frame rate
                clock.tick(60)
                if score > 10:
                    running = False
                    winning_screen = pygame.Surface((800, 600))  # Adjust the size as needed
                    winning_screen.fill((0, 0, 0))  # Fill the screen with black

                    # Display the winning screen
            if score > 10:
                winning_screen = pygame.Surface((800, 600))  # Adjust the size as needed
                winning_screen.fill((0, 0, 0))  # Fill the screen with black

                # Render the winning message and final score
                winning_text = font.render("Congrats, you have won!", True, (255, 255, 255))
                score_text = font.render(f"Your score is: {score}", True, (255, 255, 255))

                # Blit the text to the winning screen
                winning_screen.blit(winning_text, (200, 250))  # Adjust the coordinates as needed
                winning_screen.blit(score_text, (200, 300))  # Adjust the coordinates as needed

                # Blit the winning screen to the main screen
                screen.blit(winning_screen, (0, 0))

                # Update the display
                pygame.display.flip()

                # Wait for a few seconds before quitting
                pygame.time.wait(5000)
                
        elif game_mode == 'Flicker+odd':
            
            training = True
            clock = pygame.time.Clock()

            # Get a list of all pirates
            all_pirates = list(pirate_sprites.sprites())

            # Initialize current pirate and its display time
            current_pirate = random.choice(all_pirates)
            current_pirate.visible = True  # Make the current pirate visible
            pirate_display_time = pygame.time.get_ticks()

            while training:  # Continue until the game is stopped
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        training = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if current_pirate.is_clicked(pos):
                            score += 1  # Increase the score
                        elif start_button.is_clicked(pos):
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
                    current_pirate = random.choice(all_pirates)
                    current_pirate.visible = True  # Make the new pirate visible
                    pirate_display_time = pygame.time.get_ticks()

                # Clear the screen
                screen.fill((0, 0, 0))

                # Draw all pirates
                for pirate in all_pirates:
                    if pirate.visible:
                        pirate.draw_silhouette(screen)

                current_pirate.draw(screen)

                # Render the score
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                screen.blit(score_text, (10, 10))

                # Update the display
                pygame.display.flip()

                # Set the frame rate
                clock.tick(60)

            for pirate in all_pirates:
                pirate.visible = False

        else:
            None

            

        # Quit the game
        pygame.quit()