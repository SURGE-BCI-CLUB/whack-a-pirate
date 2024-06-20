# Whack-a-Pirate game by Brynn Harris-Shanks and Copilot
import pygame
import random
import numpy as np
#import psychopy
from math import sin, cos, pi
from Button import *
from Pirate import *
from Game import *
from Training import *
from Initialize import *
from Home import *

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
    Initialize.populateImgArr(f"images/pirate{i}.png", pirate_images)

sil_images = [] #Silhoutte images
for i in range(1, 7):
    Initialize.populateImgArr(f"images/white_{i}.png", sil_images)

skull_image = pygame.image.load("images/skull.jpg")
skull_image = pygame.transform.scale(skull_image, (pirate_images[0].get_width(), pirate_images[0].get_height()))

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 400 #min(screen_width, screen_height) / 2

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


# Initialize Start Game button
start_button = Button("Start Game", screen_width / 2, screen_height / 2)


# Game loop
running = True
clock = pygame.time.Clock()
    

nickname, game_mode = Home.home_page(screen, font, clock)
if nickname and game_mode:
    # Start the training phase
    Training.start_training(nickname, game_mode, pirate_sprites, screen, start_button)
    Game.game_loop(nickname, game_mode, pirate_sprites, screen, font, start_button, running, current_pirate_index, score, clock)
