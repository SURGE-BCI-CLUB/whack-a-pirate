import pygame
import sys
import csv


class Home: 
    @staticmethod
    def home_page(screen, font, clock):
        nickname = ""
        game_mode = None
        game_modes = ["Flicker-oddball", "Flicker+odd"]
        input_box = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 100, 300, 64)
        dropdown_box = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2, 300, 64)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        dropdown_active = False
        drop_text = "Select Game Mode"

        label_name = font.render("Nickname:", True, (255, 255, 255))
        label_drop = font.render("Select Mode", True, (255, 255, 255))

        while True:
            screen.fill((0, 0, 0))
            screen.blit(label_name, (input_box.x, input_box.y - label_name.get_height()))
            screen.blit(label_drop, (dropdown_box.x, dropdown_box.y - label_drop.get_height()))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            nickname = nickname[:-1]
                        else:
                            nickname += event.unicode
                    if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                        if nickname and game_mode:  # Check if both nickname and game_mode are set
                            return nickname, game_mode  # Return nickname and game_mode to start the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dropdown_active:
                        for i, mode in enumerate(game_modes):
                            rect = pygame.Rect(dropdown_box.x, dropdown_box.y + 32 * (i+1), dropdown_box.width, dropdown_box.height)
                            if rect.collidepoint(event.pos):
                                game_mode = mode
                                print(mode)
                                
                                drop_text = mode   # Update the drop_text variable with the selected mode

                                dropdown_active = False
                            
                    if input_box.collidepoint(event.pos):
                        active = not active
                        dropdown_active = False
                    elif dropdown_box.collidepoint(event.pos):
                        dropdown_active = not dropdown_active
                    else:
                        active = False
                        dropdown_active = False
                    color = color_active if active else color_inactive

                if dropdown_active:
                    for i, mode in enumerate(game_modes):
                        text = font.render(mode, True, (255, 255, 255))
                        rect = pygame.Rect(dropdown_box.x, dropdown_box.y + 32 * (i+1), dropdown_box.width, dropdown_box.height)
                        pygame.draw.rect(screen, color, rect, 2)
                        screen.blit(text, (rect.x, rect.y))

                txt_surface = font.render(nickname, True, color)
                screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                pygame.draw.rect(screen, color, input_box, 2)

                dropdown_text = font.render(drop_text, True, (255, 255, 255))
                screen.blit(dropdown_text, (dropdown_box.x+5, dropdown_box.y+5))
                pygame.draw.rect(screen, color, dropdown_box, 2)

                pygame.display.flip()
                clock.tick(60)
                