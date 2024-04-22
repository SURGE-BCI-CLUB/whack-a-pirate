import pygame
import random
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

# Define the number of locations and the distance from the center
num_locations = 6
dist_from_ctr = 400#min(screen_width, screen_height) / 2
locations = ()

# Define Pirate class
# Define Pirate class
class Pirate(pygame.sprite.Sprite):
    def __init__(self, image, location):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.location = location
        self.visible = False
        self.update()

    def update(self):
        self.rect.x = self.location[0] - self.rect.width / 2
        self.rect.y = self.location[1] - self.rect.height / 2

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

# Create pirate sprites
# Create pirate sprites with fixed locations
pirate_sprites = pygame.sprite.Group()
for i, image in enumerate(pirate_images):
    angle = 2 * pi * i / num_locations  # Distribute pirates evenly around a circle
    x = dist_from_ctr * cos(angle) + screen_width / 2
    y = screen_height / 2 - dist_from_ctr * sin(angle)  # Invert the y-coordinate
    location = (x, y)
    pirate = Pirate(image, location)
    pirate_sprites.add(pirate)

# Initialize score and timer
score = 0
timer = pygame.time.get_ticks()

# Create a font object
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for pirate in pirate_sprites:
                if pirate.rect.collidepoint(pos) and pirate.visible:
                    score += 1
                    pirate.visible = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check if the key is the Esc key
                running = False

    # Update pirate visibility
    current_time = pygame.time.get_ticks()
    if current_time - timer > 2000:  # 2 seconds have passed
        for pirate in pirate_sprites:
            pirate.visible = False
        random.choice(pirate_sprites.sprites()).visible = True
        timer = current_time

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw pirate sprites
    for pirate in pirate_sprites:
        pirate.draw(screen)

    # Render the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit() 

