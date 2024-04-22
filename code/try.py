import pygame
import random
import numpy as np
from math import sin, cos, pi

# Initialize Pygame
pygame.init()

# Get the screen resolution
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Set the screen dimensions and make it fullscreen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Whack-a-Pirate")

# Load pirate images
pirate_images = []
for i in range(1, 7):
    pirate_image = pygame.image.load(f"images/pirate{i}.png")
    pirate_images.append(pirate_image)

skull_image = pygame.image.load("images/skull.jpg")
skull_image = pygame.transform.scale(skull_image, (pirate_image.get_width(), pirate_image.get_height()))

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 400#min(screen_width, screen_height) / 2
locations = ()

#freqs
refresh_rate = pygame.display.Info().current_h
frames_per_cycle = range(10, 90 + 1,2)
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


# Define Pirate class
class Pirate(pygame.sprite.Sprite):
    def __init__(self, image, skull_image, location, duration):
        super().__init__()
        self.image = image
        self.skull_image = skull_image
        self.rect = self.image.get_rect()
        self.duration = duration
        self.location = location
        self.visible = False
        self.clicked = False

    def update(self):
        if self.location is not None:
            self.rect.x = self.location[0] - self.rect.width / 2
            self.rect.y = self.location[1] - self.rect.height / 2

    def draw(self, surface):
        if self.visible:
            if self.clicked:
                surface.blit(self.skull_image, self.rect)
            else:
                surface.blit(self.image, self.rect)

# Calculate the cycle durations for each frequency (1/frequency)
durations = [1.0/freq for freq in actual_freqs]

random.shuffle(durations)
pirates = [Pirate(image, skull_image, None, duration) for image, duration in zip(pirate_images, durations)]

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
font = pygame.font.Font(None, 36)

current_pirate_index = 0

# Game loop
running = True
clock = pygame.time.Clock()
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
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()

