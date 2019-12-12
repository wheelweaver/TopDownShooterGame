import pygame
import random

WIDTH  = 500
HEIGHT = 500
FPS = 30

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


# initalize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FINAL PROJECT")
clock = pygame.time.Clock()


# Game loop
keepGoing = True
while keepGoing:
    # keeps loop runnign at right speed
    clock.tick(FPS)
    # Process inputs (events)
    for event in pygame.event.get():
        # closing window
        if event.type == pygame.QUIT:
            keepGoing = False

    # Update


    # Draw / render
    screen.fill(BLACK)
    self.all_sprites.draw(start_screen )
    # *after* drwaing everything , flips the display (like a blackboard)
    pygame.display.flip()


pygame.quit()
