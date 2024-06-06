# Whack-a-Pirate game by Brynn Harris-Shanks and Copilot
import pygame
import random
import sys
import numpy as np
#import psychopy
from math import sin, cos, pi
from Button import *
from Pirate import *
from Game import *
from Training import *

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

sil_images = [] #Silhoutte images
for i in range(1, 7):
    sil_image = pygame.image.load(f"images/white_{i}.png")
    sil_images.append(sil_image)

skull_image = pygame.image.load("images/skull.jpg")
skull_image = pygame.transform.scale(skull_image, (pirate_image.get_width(), pirate_image.get_height()))

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 400 #min(screen_width, screen_height) / 2
locations = ()

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


# Initialize Start Game button
start_button = Button("Start Game", screen_width / 2, screen_height / 2)


# Game loop
running = True
clock = pygame.time.Clock()
    

nickname, game_mode = home_page(screen, font)
if nickname and game_mode:
    # Start the training phase
    Training.start_training(nickname, game_mode, pirate_sprites, screen, start_button)
    Game.game_loop(nickname, game_mode, pirate_sprites, screen, font, start_button, running, current_pirate_index, score, clock)
