# Whack-a-Pirate game by Brynn Harris-Shanks and Copilot
import pygame
import random
import sys
import numpy as np
#import psychopy
from math import sin, cos, pi
from Button import *
from Pirate import *

# Initialize Pygame
pygame.init()

# Get the screen resolution
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Set the screen dimensions and make it fullscreen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Whack-a-Pirate")



# Load images
pirate_images = []
for i in range(1, 7):
    pirate_image = pygame.image.load(f"images/pirate{i}.png")
    pirate_images.append(pirate_image)

sil_images = []
for i in range(1, 7):
    sil_image = pygame.image.load(f"images/white_{i}.png")
    sil_images.append(sil_image)

skull_image = pygame.image.load("images/skull.jpg")
skull_image = pygame.transform.scale(skull_image, (pirate_image.get_width(), pirate_image.get_height()))

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 400 #min(screen_width, screen_height) / 2
locations = ()

# # get the actual refresh rate of the monitor, in FPS
# refresh_rate = win.getActualFrameRate(nIdentical=10, nWarmUpFrames=10)
# win.close()
# # if refresh_rate is None:
# #     refresh_rate = 60.0  # if the previous method failed
# print('Measured monitor refresh rate: %10.3f Hz' % refresh_rate)

# # If refresh rate can't produce the exact requested highlight_duration, round to nearest possible
# frames_per_highlight = round(highlight_duration * refresh_rate)   
# print('Requested highlight duration: ', highlight_duration, ' ms')
# highlight_duration = frames_per_highlight / refresh_rate 
# print('Actual highlight duration: ', round(highlight_duration, 4), ' ms')

#freqs
refresh_rate = 240
frames_per_cycle = range(10, 40 + 1,2)
viable_freqs = np.array([refresh_rate / f for f in frames_per_cycle])

num_freqs = num_locations
median_alpha = 12
flicker_freqs = []

while len(flicker_freqs) < num_freqs:
    diff = viable_freqs - median_alpha
    diff = np.abs(diff)
    min_diff = np.min(diff)
    min_diff_idx = np.argmin(diff)
    min_diff_freq = viable_freqs[min_diff_idx]
    flicker_freqs.append(min_diff_freq)
    viable_freqs = np.delete(viable_freqs, min_diff_idx)

# compute frames per cycle for each flicker_freqs
frames_per_cycle = [round(refresh_rate / freq) for freq in flicker_freqs]
np.random.shuffle(frames_per_cycle)

actual_freqs = [refresh_rate / frames for frames in frames_per_cycle]
print('Actual flicker frequencies = ', sorted(actual_freqs))

# Calculate the cycle durations for each frequency (1/frequency)
# Calculate the cycle durations for each frequency (1/frequency)


# Calculate the cycle durations for each frequency (1/frequency)
durations = [1.0/freq for freq in actual_freqs]

random.shuffle(durations)
pirates = [Pirate(image, sil, skull_image, None, duration) for image, sil, duration in zip(pirate_images, sil_images, durations)]

# Create pirate sprites with fixed locations
pirate_sprites = pygame.sprite.Group()
for i, pirate in enumerate(pirates):
    angle = 2 * pi * i / num_locations  # Distribute pirates evenly around a circle
    x = dist_from_ctr * cos(angle) + screen_width / 2
    y = screen_height / 2 - dist_from_ctr * sin(angle)  # Invert the y-coordinate
    pirate.location = (x, y)
    pirate.update()  # Update the rect attribute based on the new location
    pirate_sprites.add(pirate)

# Initialize score and timer
score = 0
timer = pygame.time.get_ticks()

# # Create a font object
# font = pygame.font.Font(None, 50)

# current_pirate_index = 0
# clock = pygame.time.Clock()
# def home_page(screen, font):
#     nickname = ""
#     game_mode = None
#     game_modes = ["Flicker-oddball", "Flicker+odd"]
#     input_box = pygame.Rect(screen.get_width() // 2 - 70, screen.get_height() // 2 - 50, 140, 32)
#     dropdown_box = pygame.Rect(screen.get_width() // 2 - 70, screen.get_height() // 2, 140, 32)
#     start_button = pygame.Rect(screen.get_width() - 150, screen.get_height() - 50, 140, 32)
#     color_inactive = pygame.Color('lightskyblue3')
#     color_active = pygame.Color('dodgerblue2')
#     color = color_inactive
#     active = False
#     dropdown_active = False

# Create a font object
font = pygame.font.Font(None, 50)

current_pirate_index = 0
clock = pygame.time.Clock()
def home_page(screen, font):
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
    drop_text = "V"

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



#training phase


# Initialize Start Game button
start_button = Button("Start Game", screen_width / 2, screen_height / 2)

# Training period
# Training period
def start_training(nickname,game_mode):
        # Get a list of all pirates and shuffle it
    all_pirates = list(pirate_sprites.sprites())
    random.shuffle(all_pirates)

    if game_mode == "Flicker-oddball":

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


# Game loop
running = True
clock = pygame.time.Clock()

def game_loop(nickname,game_mode):
    global current_pirate_index
    global score
    global clock

    
    if game_mode == 'Flicker-oddball':
        global running

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

nickname, game_mode = home_page(screen, font)
if nickname and game_mode:
    # Start the training phase
    start_training(nickname, game_mode)
    game_loop(nickname, game_mode)


