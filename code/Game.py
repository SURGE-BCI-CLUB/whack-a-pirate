import pygame
import random
import sys
import numpy as np
import csv
from math import sin, cos, pi
from Button import *
from Pirate import *
from Saveinfo import *
from Scoreboard import *

class Game:
    
    @staticmethod
    def game_loop(nickname,game_mode, pirate_sprites, screen, font, start_button, running, current_pirate_index, score, clock):
        
        
        if game_mode == 'Flicker':
            game_start_time = pygame.time.get_ticks()
            start_time = pygame.time.get_ticks()
            while running:
                current_time = pygame.time.get_ticks()
                
                if current_time - game_start_time >= 60000:
                    running = False
                    Saveinfo.save_user_score_to_csv(nickname, score)
                    screen.fill((0, 0, 0)) 
                    pygame.display.flip() 
                    scoreboard = Scoreboard()
                    scores = Scoreboard.read_scores_from_csv('user_scores.csv')
                    Scoreboard.display_scoreboard(screen, scores)
                    pygame.time.wait(5000) 
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for pirate in pirate_sprites.sprites():
                            if pirate.rect.collidepoint(pos) and pirate.visible:
                                score += 1
                                pirate.clicked = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                            running = False
                
                # Update pirate visibility for all pirates simultaneously
                if current_time - start_time < 2000:  # 2 seconds have not passed
                    for pirate in pirate_sprites.sprites():
                        if not pirate.clicked:  # Only update visibility if pirate has not been clicked
                            phase = ((current_time - start_time) % (pirate.duration * 1000)) / (pirate.duration * 1000)
                            pirate.visible = np.sin(2 * np.pi * phase) > 0
                else:
                    for pirate in pirate_sprites.sprites():
                        pirate.visible = False
                        pirate.clicked = False  # Reset clicked status
                    start_time = current_time

                # Clear the screen
                screen.fill((0, 0, 0))

                # Draw all visible pirates
                for pirate in pirate_sprites.sprites():
                    if pirate.visible:
                        pirate.draw(screen)

                # Render the score
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                user_text = font.render(f"User: {nickname}", True, (255, 255, 255))
                screen.blit(user_text, (10, 40))
                screen.blit(score_text, (10, 10))

                # Update the display
                pygame.display.flip()

                # Set the frame rate
                clock.tick(60)

                
        elif game_mode == 'Testing':
            game_start_time = pygame.time.get_ticks()
            start_time = pygame.time.get_ticks()
            while running:
                current_time = pygame.time.get_ticks()
                
                if current_time - game_start_time >= 60000:
                    running = False
                    Saveinfo.save_user_score_to_csv(nickname, score)
                    screen.fill((0, 0, 0)) 
                    pygame.display.flip() 
                    scoreboard = Scoreboard()
                    scores = Scoreboard.read_scores_from_csv('user_scores.csv')
                    Scoreboard.display_scoreboard(screen, scores)
                    pygame.time.wait(5000) 
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for pirate in pirate_sprites.sprites():
                            if pirate.rect.collidepoint(pos) and pirate.visible:
                                score += 1
                                pirate.clicked = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                            running = False
                
                # Update pirate visibility for all pirates simultaneously
                if current_time - start_time < 2000:  # 2 seconds have not passed
                    for pirate in pirate_sprites.sprites():
                        if not pirate.clicked:  # Only update visibility if pirate has not been clicked
                            phase = ((current_time - start_time) % (pirate.duration * 1000)) / (pirate.duration * 1000)
                            pirate.visible = np.sin(2 * np.pi * phase) > 0
                else:
                    for pirate in pirate_sprites.sprites():
                        pirate.visible = False
                        pirate.clicked = False  # Reset clicked status
                    start_time = current_time

                # Clear the screen
                screen.fill((0, 0, 0))

                # Draw all visible pirates
                for pirate in pirate_sprites.sprites():
                    if pirate.visible:
                        pirate.draw(screen)

                # Render the score
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                user_text = font.render(f"User: {nickname}", True, (255, 255, 255))
                screen.blit(user_text, (10, 40))
                screen.blit(score_text, (10, 10))

                # Update the display
                pygame.display.flip()

                # Set the frame rate
                clock.tick(60)

        else:
            None

            

        # Quit the game
        pygame.quit()