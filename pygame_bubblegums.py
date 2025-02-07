from support_functions import *
import pygame
import numpy as np

rows, columns = 27, 19
TSP = TSPDecoder(rows=rows, columns=columns)

# Define constants
PIXEL_WIDTH = 20
PIXEL_HEIGHT = 10
PIXEL_MARGIN = 2
BLACK = (0, 0, 0)
BUBBLEGUM_COLOR = (255, 105, 180)  # Pink color
TOUCH_THRESHOLD = 50  # Adjust based on sensor sensitivity
BUBBLEGUM_LIFESPAN = 60  # Frames before bubblegum disappears
GROWTH_RATE = 1.5  # Growth per frame
MAX_BUBBLE_SIZE = 50  # Bubbles pop at this size

# Initialise PyGame
pygame.init()
WINDOW_SIZE = [
    columns * PIXEL_WIDTH + columns * PIXEL_MARGIN + 2 * PIXEL_MARGIN,
    rows * PIXEL_HEIGHT + rows * PIXEL_MARGIN + 2 * PIXEL_MARGIN
]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Bubblegum Example")

# Initialise the PyGame Clock for timing
clock = pygame.time.Clock()
grid = np.zeros((TSP.rows, TSP.columns))

# Dictionary to track bubbles with coordinates as keys
bubblegums = {}

while True:
    # Check if the screen is closed and quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get the frame
    if TSP.frame_available:
        grid = TSP.readFrame()

    # Clear the screen
    screen.fill(BLACK)

    # Loop through all pixels in the frame
    for row in range(rows):
        for column in range(columns):
            # Get the pixel value and set the gray value accordingly
            pixel = grid[row][column]
            color = (pixel, pixel, pixel)

            # Draw the pixel on the screen
            pygame.draw.rect(
                screen,
                color,
                [
                    PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_WIDTH) * column),
                    PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_HEIGHT) * row),
                    PIXEL_WIDTH,
                    PIXEL_HEIGHT
                ]
            )

            # Detect touches and add/update bubblegums
            if pixel > TOUCH_THRESHOLD:
                x = PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_WIDTH) * column) + PIXEL_WIDTH // 2
                y = PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_HEIGHT) * row) + PIXEL_HEIGHT // 2
                key = (x, y)

                if key not in bubblegums:
                    bubblegums[key] = [x, y, 2]  # Start small

    # Update and draw bubblegums
    updated_bubblegums = {}

    for key, (x, y, size) in bubblegums.items():
        row = (y - PIXEL_MARGIN) // (PIXEL_MARGIN + PIXEL_HEIGHT)
        col = (x - PIXEL_MARGIN) // (PIXEL_MARGIN + PIXEL_WIDTH)

        if 0 <= row < rows and 0 <= col < columns and grid[row][col] > TOUCH_THRESHOLD:
            new_size = size + GROWTH_RATE
            if new_size < MAX_BUBBLE_SIZE:
                updated_bubblegums[key] = [x, y, new_size]
                pygame.draw.circle(screen, BUBBLEGUM_COLOR, (x, y), int(new_size))

    bubblegums = updated_bubblegums  # Remove popped bubbles

    # Limit the framerate to 60FPS
    clock.tick(60)

    # Draw to the display
    pygame.display.flip()
