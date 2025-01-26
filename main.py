import pygame

pygame.init()  # Initialize pygame

# Load image to create a window
image = pygame.image.load("image.png")
window = pygame.display.set_mode(image.get_size())

running = True

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # First, if user wants to quit
            running = False
            break
        elif event.type == pygame.KEYDOWN: # Else, if user pressed keyboard
            # User wants to quit game
            if event.key == pygame.K_ESCAPE:
                running = False
                break
    # Rendering
    window.blit(image, (0, 0))
    pygame.display.update()

pygame.quit()